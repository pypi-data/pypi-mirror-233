import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm

import logging
from typing import Optional, Callable, Union

from .tools import VerboseBase

g_device = "cuda:0" if torch.cuda.is_available() else "cpu"

class dl_trainer:
    """A torch model trainer

    Parameters
    ----------
    model: torch.nn.Module
        The model to be trained
    loss: Callable[[torch.nn.tensor, torch.nn.tensor], torch.tensor]
        The loss function
    optimizer: torch.optim.Optimizer
        The BP optimizer
    epoch: int
        Number of epochs to train
    lr: float,
        The learning rate
    lr_scheduler: Optional[Callable[[int], float]], default `None`
        A function that computes a multiplicative factor given an integer parameter epoch, `None`
    to disable
    batch_size: Union[int, Callable[[int], int]], default `64`
        A function that computes batch size given an integer parameter epoch, or a constant batch
    size, only enable when passing a
    `torch.utils.data.Dataset` to the trainer
    mini_batch: Union[int, Callable[[int], int]], default `1`
        A function that computes mini batch size given an integer parameter epoch, or a constant
    mini batch size, useful when you have a small GPU
    memory size but want much larger batch sizes
    patience: int, default `-1`:
        The patience parameter for early stopping, set to `-1` to disable
    delta: float, default `0`:
        The minimal loss improvement required for the model to be considered improving
    logger: Optional[logging.Logger], default `None`
        A logger for debug-level information
    verbose: Optional[VerboseBase], default `None`
        The verbose evaluator for epoch level data
    eval_train: bool, default `False`
        Whether to eval the train set every epoch
    device: torch.device, default `"cuda:0" if torch.cuda.is_available() else "cpu"`
        On which device to train the model
    *args, **kwargs:
        Additional args for optimizer
    """
    def __init__(self,
                 model: nn.Module,
                 loss: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
                 optimizer: torch.optim.Optimizer,
                 epoch: int,
                 lr: float,
                 lr_scheduler: Optional[Callable[[int], float]] = None,
                 batch_size: Union[int, Callable[[int], int]] = 64,
                 mini_batch: Union[int, Callable[[int], int]] = 1,
                 patience: int = -1,
                 delta: float = 0,
                 logger: Optional[logging.Logger] = None,
                 verbose: Optional[VerboseBase] = None,
                 eval_train: bool = False,
                 device: torch.device = "cuda:0" if torch.cuda.is_available() else "cpu",
                 *args, **kwargs,
                 ) -> None:
        self.model = model
        self.loss = loss
        self.lr = lr
        self.optimizer = optimizer(self.model.parameters(), lr=lr, *args, **kwargs)
        self.epoch = epoch
        self.lr_lambda = lr_scheduler
        self.lr_scheduler = torch.optim.lr_scheduler.LambdaLR(self.optimizer, lr_lambda=lr_scheduler) if lr_scheduler is not None else None
        self.batch_size = batch_size
        self.mini_batch = mini_batch
        self.patience = patience
        self.delta = delta
        self.logger = logger
        self.verbose = verbose
        self.eval_train = eval_train
        self.device = device

    def train(self,
              train_data: Union[Dataset, DataLoader],
              valid_data: Union[Dataset, DataLoader],
              *args, **kwargs) -> None:
        """Train the model

        Parameters
        ----------
        train_data: Union[Dataset, DataLoader]
            The training data
        valid_date: Union[Dataset, DataLoader]
            The validation data
        *args, **kwargs:
            Additional parameters for `torch.utils.data.DataLoader` if passing a `torch.utils.data.Dataset`
        """
        torch.cuda.empty_cache()
        self.model.to(self.device)
        best_loss, best_metric, patience = np.inf, np.inf, self.patience
        self.model.to(self.device)
        for EPOCH in tqdm(range(self.epoch), desc="training", unit="epoch"):
            if self.logger:
                self.logger.debug(f"Starting train epoch {EPOCH}.") # DEBUG LOG
            self.train_epoch(EPOCH, train_data, *args, **kwargs)
            if self.logger:
                self.logger.debug(f"Train epoch {EPOCH} finished.") # DEBUG LOG
            if self.eval_train:
                if self.logger:
                    self.logger.debug(f"Evaluating training epoch {EPOCH}.") # DEBUG LOG
                self.eval_epoch(EPOCH, train_data, *args, **kwargs)
                if self.verbose is not None:
                    self.verbose.epoch_end(EPOCH, "train")
            if self.logger:
                self.logger.debug(f"Starting valid epoch {EPOCH}.") # DEBUG LOG
            loss = self.eval_epoch(EPOCH, valid_data, *args, **kwargs)
            if self.logger:
                self.logger.debug(f"Valid epoch {EPOCH} finished, current loss is {loss:.8f}.") # DEBUG LOG
            patience = patience - 1
            if self.verbose is not None:
                metric = self.verbose.epoch_end(EPOCH, "valid")
                if self.logger and metric is not None:
                    self.logger.debug(f"Verbose enabled, verbose metric {metric:.8f}.") # DEBUG LOG
                if metric is not None and metric < best_metric:
                    if self.logger and metric is not None:
                        self.logger.debug(f"Metric update {best_metric:.8f} -> {metric:.8f}.") # DEBUG LOG
                    best_metric = metric
                    patience = self.patience
            if loss < best_loss - self.delta:
                if self.logger:
                    self.logger.debug(f"Loss update {best_loss:.8f} -> {loss:.8f}.") # DEBUG LOG
                best_loss = loss
                patience = self.patience
            if self.logger and self.patience >= 0:
                self.logger.debug(f"Current patience {patience}.") # DEBUG LOG
            if patience == 0:
                break

            if self.lr_scheduler is not None:
                self.lr_scheduler.step()

    def train_epoch(self,
                    epoch: int,
                    train_data: Union[Dataset, DataLoader],
                    *args, **kwargs
                    ) -> None:
        if isinstance(train_data, DataLoader):
            if self.logger:
                self.logger.debug(f"Current lr = {self.lr}{f' * {self.lr_lambda(epoch)}' if self.lr_lambda else ''}, mini batch = {self.mini_batch if isinstance(self.mini_batch, int) else self.mini_batch(epoch)}.")
            train_loader = train_data
        elif isinstance(self.batch_size, int):
            if self.logger:
                self.logger.debug(f"Current lr = {self.lr}{f' * {self.lr_lambda(epoch)}' if self.lr_lambda else ''}, batch size = {self.batch_size}, mini batch = {self.mini_batch if isinstance(self.mini_batch, int) else self.mini_batch(epoch)}.")
            train_loader = DataLoader(train_data, batch_size=self.batch_size, *args, **kwargs)
        elif callable(self.batch_size):
            if self.logger:
                self.logger.debug(f"Current lr = {self.lr}{f' * {self.lr_lambda(epoch)}' if self.lr_lambda else ''}, batch size = {self.batch_size(epoch)}, mini batch = {self.mini_batch if isinstance(self.mini_batch, int) else self.mini_batch(epoch)}.")
            train_loader = DataLoader(train_data, batch_size=self.batch_size(epoch), *args, **kwargs)
        else:
            raise ValueError
        mini_batch, countr = self.mini_batch if isinstance(self.mini_batch, int) else self.mini_batch(epoch), 0
        self.model.train()
        for x, y in train_loader:
            x, y = x.to(self.device), y.to(self.device)
            yhat = self.model(x)
            loss = self.loss(yhat, y) / mini_batch
            if countr == 0:
                self.optimizer.zero_grad()
            loss.backward()
            countr = countr + 1
            if countr == mini_batch:
                self.optimizer.step()
                countr = 0
        if countr != 0:
            self.optimizer.step()

    def eval_epoch(self,
                   epoch: int,
                   valid_data: Union[Dataset, DataLoader],
                   *args, **kwargs
                   ) -> None:
        if isinstance(valid_data, DataLoader):
            valid_loader = valid_data
        elif isinstance(self.batch_size, int):
            valid_loader = DataLoader(valid_data, batch_size=self.batch_size, *args, **kwargs)
        elif callable(self.batch_size):
            valid_loader = DataLoader(valid_data, batch_size=self.batch_size(epoch), *args, **kwargs)
        else:
            raise ValueError
        accum_loss, accum_batch = 0, 0
        self.model.eval()
        with torch.no_grad():
            for x, y in valid_loader:
                x, y = x.to(self.device), y.to(self.device)
                yhat = self.model(x)
                loss = self.loss(yhat, y)
                accum_loss = accum_loss + loss.data * y.shape[0]
                accum_batch = accum_batch + y.shape[0]
                if self.verbose is not None:
                    self.verbose.eval_iter(yhat=yhat, y=y)
        return accum_loss / accum_batch
