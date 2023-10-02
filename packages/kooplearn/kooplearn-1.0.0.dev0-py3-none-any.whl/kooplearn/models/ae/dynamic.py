import logging
import os
import pickle
import weakref
from copy import deepcopy
from pathlib import Path
from typing import Callable, Optional, Union

import numpy as np
from scipy.linalg import eig

from kooplearn._src.check_deps import check_torch_deps
from kooplearn._src.utils import ShapeError, check_contexts_shape, check_is_fitted
from kooplearn.abc import BaseModel
from kooplearn.models.ae.utils import (
    decode_contexts,
    encode_contexts,
    evolve_batch,
    evolve_contexts,
)

logger = logging.getLogger("kooplearn")
check_torch_deps()
import lightning  # noqa: E402
import torch  # noqa: E402


class DynamicAE(BaseModel):
    def __init__(
        self,
        encoder: torch.nn.Module,
        decoder: torch.nn.Module,
        latent_dim: int,
        optimizer_fn: torch.optim.Optimizer,
        optimizer_kwargs: dict,
        trainer: lightning.Trainer,
        loss_weights: dict = {"rec": 1.0, "pred": 1.0, "lin": 1.0},
        encoder_kwargs: dict = {},
        decoder_kwargs: dict = {},
        use_lstsq_for_evolution: bool = False,  # If true, implements "Deep Dynamical Modeling and Control of Unsteady Fluid Flows" by Morton et al. (2018)
        seed: Optional[int] = None,
    ):
        lightning.seed_everything(seed)
        self.lightning_trainer = trainer
        self.lightning_module = DynamicAEModule(
            encoder,
            decoder,
            latent_dim,
            optimizer_fn,
            optimizer_kwargs,
            loss_weights=loss_weights,
            encoder_kwargs=encoder_kwargs,
            decoder_kwargs=decoder_kwargs,
            use_lstsq_for_evolution=use_lstsq_for_evolution,
            kooplearn_model_weakref=weakref.ref(self),
        )
        self.seed = seed
        self._is_fitted = False
        # Todo: Add warning on lookback_len for this model

    def fit(
        self,
        train_dataloaders=None,
        val_dataloaders=None,
        datamodule: Optional[lightning.LightningDataModule] = None,
        ckpt_path: Optional[str] = None,
    ):
        """Fits the Koopman AutoEncoder model. Accepts the same arguments as :meth:`lightning.Trainer.fit`, except for the ``model`` keyword, which is automatically set internally.

        Args:
            train_dataloaders: An iterable or collection of iterables specifying training samples.
                Alternatively, a :class:`~lightning.pytorch.core.datamodule.LightningDataModule` that defines
                the :class:`~lightning.pytorch.core.hooks.DataHooks.train_dataloader` hook.

            val_dataloaders: An iterable or collection of iterables specifying validation samples.

            datamodule: A :class:`~lightning.pytorch.core.datamodule.LightningDataModule` that defines
                the :class:`~lightning.pytorch.core.hooks.DataHooks.train_dataloader` hook.

            ckpt_path: Path/URL of the checkpoint from which training is resumed. Could also be one of two special
                keywords ``"last"`` and ``"hpc"``. If there is no checkpoint file at the path, an exception is raised.
        """
        if isinstance(train_dataloaders, lightning.LightningDataModule):
            datamodule = train_dataloaders
            train_dataloaders = None

        # If you supply a datamodule you can't supply train_dataloader or val_dataloaders
        if (
            train_dataloaders is not None or val_dataloaders is not None
        ) and datamodule is not None:
            raise ValueError(
                "You cannot pass `train_dataloader` or `val_dataloaders` to `VAMPNet.fit(datamodule=...)`"
            )
        # Get the shape of the first batch to determine the lookback_len
        if train_dataloaders is None:
            assert isinstance(datamodule, lightning.LightningDataModule)
            for batch in datamodule.train_dataloader():
                with torch.no_grad():
                    self.lightning_module.dry_run(batch)
                    self._state_trail_dims = tuple(batch.shape[2:])
                break
        else:
            assert isinstance(train_dataloaders, torch.utils.data.DataLoader)
            for batch in train_dataloaders:
                with torch.no_grad():
                    self.lightning_module.dry_run(batch)
                    self._state_trail_dims = tuple(batch.shape[2:])
                break

        self.lightning_trainer.fit(
            model=self.lightning_module,
            train_dataloaders=train_dataloaders,
            val_dataloaders=val_dataloaders,
            datamodule=datamodule,
            ckpt_path=ckpt_path,
        )
        self._is_fitted = True

    def _np_to_torch(self, data: np.ndarray):
        check_contexts_shape(data, self.lookback_len, is_inference_data=True)
        model_device = self.lightning_module.device
        return torch.from_numpy(data.copy()).float().to(model_device)

    def predict(
        self,
        data: np.ndarray,
        t: int = 1,
        observables: Optional[Union[Callable, np.ndarray]] = None,
    ):
        torch_data = self._np_to_torch(
            data
        )  # [n_samples, context_len == 1, *trail_dims]
        check_is_fitted(self, ["_state_trail_dims"])
        assert tuple(torch_data.shape[2:]) == self._state_trail_dims

        with torch.no_grad():
            init_data = torch_data[:, self.lookback_len - 1, ...]
            evolved_data = evolve_batch(
                init_data,
                t,
                self.lightning_module.encoder,
                self.lightning_module.decoder,
                self.lightning_module.evolution_operator,
            )
            evolved_data = evolved_data.detach().cpu().numpy()
        if observables is None:
            return evolved_data
        elif callable(observables):
            return observables(evolved_data)
        else:
            raise NotImplementedError(
                "Only callable observables or None are supported at the moment."
            )

    def modes(
        self,
        data: np.ndarray,
        observables: Optional[Union[Callable, np.ndarray]] = None,
    ):
        raise NotImplementedError()

    def eig(
        self,
        eval_left_on: Optional[np.ndarray] = None,
        eval_right_on: Optional[np.ndarray] = None,
    ):
        if hasattr(self, "_eig_cache"):
            w, vl, vr = self._eig_cache
        else:
            if self.lightning_module.hparams.use_lstsq_for_evolution:
                raise NotImplementedError(
                    f"Eigenvalues and eigenvectors are not implemented when {self.lightning_module.hparams.use_lstsq_for_evolution} == True."
                )
            else:
                K = self.lightning_module.evolution_operator
                K_np = K.detach().cpu().numpy()
                w, vl, vr = eig(K_np, left=True, right=True)
                self._eig_cache = w, vl, vr

        if eval_left_on is None and eval_right_on is None:
            # (eigenvalues,)
            return w
        else:
            raise NotImplementedError(
                "Left / right eigenfunction evaluations are not implemented yet."
            )

    # TODO: Test
    def save(self, path: os.PathLike):
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        # Save the trainer
        torch.save(self.lightning_trainer, path / "lightning_trainer.bin")
        # Save the lightning checkpoint
        ckpt = path / "lightning.ckpt"
        self.lightning_trainer.save_checkpoint(str(ckpt))
        del self.lightning_module
        del self.lightning_trainer
        model = path / "kooplearn_model.pkl"
        with open(model, "wb") as f:
            pickle.dump(self, f)

    # TODO: Test
    @classmethod
    def load(cls, path: os.PathLike):
        path = Path(path)
        trainer = torch.load(path / "lightning_trainer.bin")
        ckpt = path / "lightning.ckpt"
        with open(path / "kooplearn_model.pkl", "rb") as f:
            restored_obj = pickle.load(f)
        assert isinstance(restored_obj, cls)
        restored_obj.lightning_trainer = trainer
        restored_obj.lightning_module = DynamicAEModule.load_from_checkpoint(str(ckpt))
        return restored_obj

    @property
    def is_fitted(self) -> bool:
        return self._is_fitted

    @property
    def lookback_len(self) -> int:
        return 1


class DynamicAEModule(lightning.LightningModule):
    def __init__(
        self,
        encoder: torch.nn.Module,
        decoder: torch.nn.Module,
        latent_dim: int,
        optimizer_fn: torch.optim.Optimizer,
        optimizer_kwargs: dict,
        loss_weights: dict = {"rec": 1.0, "pred": 1.0, "lin": 1.0},
        encoder_kwargs: dict = {},
        decoder_kwargs: dict = {},
        use_lstsq_for_evolution: bool = False,
        kooplearn_model_weakref: weakref.ReferenceType = None,
    ):
        super().__init__()
        self.save_hyperparameters(ignore=["kooplearn_model_weakref", "optimizer_fn"])
        self.encoder = encoder(**encoder_kwargs)
        self.decoder = decoder(**decoder_kwargs)
        if not self.hparams.use_lstsq_for_evolution:
            self._lin = torch.nn.Linear(latent_dim, latent_dim, bias=False)
            self.evolution_operator = self._lin.weight
        self._optimizer = optimizer_fn
        _tmp_opt_kwargs = deepcopy(optimizer_kwargs)
        if "lr" in _tmp_opt_kwargs:  # For Lightning's LearningRateFinder
            self.lr = _tmp_opt_kwargs.pop("lr")
            self.opt_kwargs = _tmp_opt_kwargs
        else:
            raise ValueError(
                "You must specify a learning rate 'lr' key in the optimizer_kwargs."
            )
        self._kooplearn_model_weakref = kooplearn_model_weakref

    def _lstsq_evolution(self, batch: torch.Tensor):
        X = batch[:, 0, ...]
        Y = batch[:, 1, ...]
        return (torch.linalg.lstsq(X, Y).solution).T

    def configure_optimizers(self):
        kw = self.opt_kwargs | {"lr": self.lr}
        return self._optimizer(self.parameters(), **kw)

    def training_step(self, train_batch, batch_idx):
        lookback_len = self._kooplearn_model_weakref().lookback_len
        encoded_batch = encode_contexts(train_batch, self.encoder)
        if self.hparams.use_lstsq_for_evolution:
            K = self._lstsq_evolution(encoded_batch)
        else:
            K = self.evolution_operator
        evolved_batch = evolve_contexts(encoded_batch, lookback_len, K)
        decoded_batch = decode_contexts(evolved_batch, self.decoder)

        MSE = torch.nn.MSELoss()
        # Reconstruction + prediction loss
        rec_loss = MSE(
            train_batch[:, lookback_len - 1, ...],
            decoded_batch[:, lookback_len - 1, ...],
        )
        pred_loss = MSE(
            train_batch[:, lookback_len:, ...], decoded_batch[:, lookback_len:, ...]
        )

        alpha_rec = self.hparams.loss_weights.get("rec", 1.0)
        alpha_pred = self.hparams.loss_weights.get("pred", 1.0)

        loss = alpha_rec * rec_loss + alpha_pred * pred_loss
        metrics = {
            "train/reconstruction_loss": rec_loss.item(),
            "train/prediction_loss": pred_loss.item(),
        }
        if not self.hparams.use_lstsq_for_evolution:
            # Linear loss
            lin_loss = MSE(encoded_batch, evolved_batch)
            metrics["train/linear_loss"] = lin_loss.item()
            alpha_lin = self.hparams.loss_weights.get("lin", 1.0)
            loss += alpha_lin * lin_loss

        metrics["train/full_loss"] = loss.item()
        self.log_dict(metrics, on_step=True, prog_bar=True, logger=True)
        return loss

    def dry_run(self, batch: torch.Tensor):
        lookback_len = self._kooplearn_model_weakref().lookback_len
        check_contexts_shape(batch, lookback_len)
        # Caution: this method is designed only for internal calling.
        Z = encode_contexts(batch, self.encoder)
        if self.hparams.use_lstsq_for_evolution:
            X = Z[:, 0, ...]
            Y = Z[:, 1, ...]
            evolution_operator = (torch.linalg.lstsq(X, Y).solution).T
        else:
            evolution_operator = self.evolution_operator
        Z_evolved = evolve_contexts(Z, lookback_len, evolution_operator)
        X_evol = decode_contexts(
            Z_evolved, self.decoder
        )  # Should fail if the shape is wrong
        assert Z.shape == Z_evolved.shape

        if batch.shape != X_evol.shape:
            raise ShapeError(
                f"The shape of the evolved states {X_evol.shape[2:]} does not match the shape of the initial states {batch.shape[2:]}. Please check that the decoder networks output tensors of the same shape as the input tensors."
            )
