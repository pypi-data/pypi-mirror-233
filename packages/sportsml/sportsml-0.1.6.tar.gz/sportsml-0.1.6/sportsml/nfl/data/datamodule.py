import dgl
import lightning.pytorch as pl
import numpy as np
import torch

from .dataset import NFLGraphDataset
from .features import GRAPH_FEATURES


class NFLGraphDataModule(pl.LightningDataModule):
    def __init__(
        self,
        df,
        val_df=None,
        test_df=None,
        feature_columns=GRAPH_FEATURES,
        target_columns=["result"],
        batch_size=64,
        split_type="random",
        splits=[0.8, 0.1, 0.1],
        num_workers=4,
    ):
        super().__init__()
        self.df = df
        self.val_df = val_df
        self.test_df = test_df
        self.feature_columns = feature_columns
        self.target_columns = target_columns
        self.batch_size = batch_size
        self.split_type = split_type
        self.splits = splits
        self.num_workers = num_workers

    def setup(self, stage="train"):
        self.ds = NFLGraphDataset(self.df, self.feature_columns, self.target_columns)
        if self.split_type == "random":
            (
                self.train_ds,
                self.val_ds,
                self.test_ds,
            ) = torch.utils.data.random_split(self.ds, self.splits)
        elif self.split_type == "time":
            idx = (len(self.ds) * np.array(self.splits).cumsum()).astype(int)[:2]
            train_idx, val_idx, test_idx = np.array_split(np.arange(len(self.ds)), idx)
            self.train_ds = torch.utils.data.Subset(self.ds, train_idx.tolist())
            self.val_ds = torch.utils.data.Subset(self.ds, val_idx.tolist())
            self.test_ds = torch.utils.data.Subset(self.ds, test_idx.tolist())
        elif self.split_type is None:
            self.train_ds = self.ds
        else:
            raise ValueError(f"split type {self.split_type} not supported")
        if self.val_df is not None:
            self.val_ds = NFLGraphDataset(
                self.val_df, self.feature_columns, self.target_columns
            )
        if self.test_df is not None:
            self.test_ds = NFLGraphDataset(
                self.test_df, self.feature_columns, self.target_columns
            )

    def train_dataloader(self):
        return dgl.dataloading.GraphDataLoader(
            self.train_ds,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
        )

    def val_dataloader(self):
        return dgl.dataloading.GraphDataLoader(
            self.val_ds,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
        )

    def test_dataloader(self):
        return dgl.dataloading.GraphDataLoader(
            self.test_ds,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
        )
