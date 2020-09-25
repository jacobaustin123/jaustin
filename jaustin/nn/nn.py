# Copyright (c) NVIDIA Corporation. All rights reserved
#
# TrainerBase is modified from the WeightedProcrustesTrainer from https://github.com/chrischoy/DeepGlobalRegistration/blob/master/core/trainer.py
# Copyright (c) Chris Choy (chrischoy@ai.stanford.edu) and Wei Dong (weidong@andrew.cmu.edu), MIT License
import os
import logging
import numpy as np
import json
import math
from typing import Union
from datetime import datetime
import sys

from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import DataLoader

eps = np.finfo(float).eps

class TrainerBase:
    def __init__(
        self,
        data_loader: DataLoader,
        val_data_loader: DataLoader,
        device,
        checkpoint: str = None,
        cfg: dict = None,
    ):
        logging.info("Initializing a trainer.")

        self.cfg = cfg

        # initialize logging
        self.checkpoint_dir = self.get_checkpoint_dir()

        logdir = os.path.join(checkpoint_dir, "debug.log")
        logging.root.handlers = []

        handlers = [
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(logdir)
        ]

        logging.basicConfig(
            level=logging.root.level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=handlers,
        )

        logging.info(f"saving log files to {logdir}.")

        self.writer = SummaryWriter(self.checkpoint_dir)
        
        # Training config and logging
        self.start_epoch, self.train_iters, self.train_steps_per_epoch = self.get_training_info()

        epoch_steps = self.train_steps_per_epoch
        self.max_epoch = int(math.ceil(self.train_iters / epoch_steps))

        # Data loader
        self.data_loader = data_loader
        self.val_data_loader = val_data_loader

        self.train_data_loader_iter = iter(self.data_loader)
        self.test_valid = True if self.val_data_loader is not None else False
        self.device = device

        # Validation config
        self.validate_every, self.best_metric, self.best_val = self.get_valid_info()
        self.best_val_epoch = -np.inf

        self.initialize_model()

        self.initialize_optimizer()
        self.initialize_scheduler()

        if checkpoint is not None:
            self.load_checkpoint(checkpoint)

        self.dump_config()

    def get_checkpoint_dir(self) -> str:
        """
        Return the checkpoint directory for the current run. For example,
        can return self.cfg.experiment_dir.
        """

        raise NotImplementedError

    def initialize_logging(self, checkpoint_dir):
        logdir = os.path.join(checkpoint_dir, "debug.log")
        logging.root.handlers = []

        handlers = [
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(logdir)
        ]

        logging.basicConfig(
            level=logging.root.level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=handlers,
        )

        logging.info(f"saving log files to {logdir}.")

    def initialize_distributed_training(self, rank) -> None:
        raise NotImplementedError

    def initialize_model(self) -> None:
        raise NotImplementedError
        # Something like this
        ModelClass = load_model(self.cfg)
        self.model_a = ModelClass(A, B, C, args).to(self.device)
        self.model_b = ModelClass(C, D, E, args).to(self.device)

    def get_training_info(self):
        """get_training_info should return self.start_epoch, self.train_iters, 
        self.train_steps_per_epoch. for example, can return self.cfg.train.start_epoch, 
        self.cfg.train.iters, self.cfg.train.train_steps_per_epoch."""

        raise NotImplementedError

    def get_valid_info(self):
        """get_val_info should return self.validate_every, self.best_metric, self.init_metric,
        where validate_every determines how many epochs to validate after, best_metric is the string
        name for the best metric returned by _valid_epoch, and init_mtric is the initial value."""
        raise NotImplementedError

        # return name of metric and initial value
        return self.cfg.valid.validate_every, "psnr", -np.inf
        

    def initialize_optimizer(self) -> None:
        raise NotImplementedError
        # Loss and optimizer
        config = self.cfg
        self.param_optimizer = getattr(optim, config.optimizer)(
            self.network.parameters(),
            lr=config.lr,
            momentum=config.momentum,
            weight_decay=config.weight_decay,
        )

    def initialize_scheduler(self) -> None:
        raise NotImplementedError

    def load_checkpoint(self, checkpoint) -> None:
        raise NotImplementedError

    def dump_config(self):
        json.dump(
            cfg,
            open(os.path.join(self.checkpoint_dir, "config.json"), "w"),
            indent=4,
            sort_keys=False,
        )

    def pre_epoch(self, epoch):
        """called at the beginning of each epoch. For example, can run
        torch.cuda.empty_cache()."""

        return

    def train(self):
        """
        Full training logic: train, valid, and save
        """
        # Train and valid
        for epoch in range(self.start_epoch, self.max_epoch + 1):
            self.pre_epoch(epoch)

            # validate
            if self.test_valid and epoch % self.validate_every == 0:
                val_dict = self._valid_epoch(epoch)

                if self.best_val < val_dict[self.best_val_metric]:
                    self.info(
                        f"Saving the best val model with {self.best_val_metric}: {val_dict[self.best_val_metric]}",
                    )
                    self.best_val = val_dict[self.best_val_metric]
                    self.best_val_epoch = epoch
                    self._save_checkpoint(epoch, "best_val_checkpoint")

                else:
                    logging.info(
                        f"Current epoch: {epoch}. best val model with {self.best_val_metric}: {self.best_val} at epoch {self.best_val_epoch}"
                    )
                    self._save_checkpoint(epoch, "checkpoint")

            self.log_scheduler(epoch)
            self._train_epoch(epoch)
            self.step_scheduler(epoch)

    def eval(self, save_disparity_image=False):
        raise NotImplementedError

    def log_scheduler(self, epoch):
        lr = self.optimizer.param_groups[0]['lr']
        logging.info(f" Epoch: {epoch}, LR: {lr}")

        self.writer.add_scalar("train/learning_rate", lr, epoch)

    def step_scheduler(self, epoch):
        self.scheduler.step()

    def step_and_zero_optimizer(self, step):
        self.optimizer.step()
        self.optimizer.zero_grad()

    def _train_epoch(self, epoch: int) -> None:
        raise NotImplementedError

    def _valid_epoch(self) -> dict:
        raise NotImplementedError

    def _save_checkpoint(self, epoch: int, filename="checkpoint") -> None:
        raise NotImplementedError