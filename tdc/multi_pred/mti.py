# -*- coding: utf-8 -*-
# Author: TDC Team
# License: MIT

import warnings

warnings.filterwarnings("ignore")
import sys

from . import bi_pred_dataset
from ..metadata import dataset_names


class MTI(bi_pred_dataset.DataLoader):
    """Data loader class to load datasets in MicroRNA-Target Interaction Prediction task.
    More info: https://tdcommons.ai/multi_pred_tasks/mti/


    Task Description: Binary Classification.
                      Given the miRNA mature sequence and target amino acid sequence,
                      predict their likelihood of interaction.

    Args:
        name (str): the dataset name.
        path (str, optional):
            The path to save the data file, defaults to './data'
        label_name (str, optional):
            For multi-label dataset, specify the label name, defaults to None
        print_stats (bool, optional):
            Whether to print basic statistics of the dataset, defaults to False

    """

    def __init__(self, name, path="./data", label_name=None, print_stats=False):
        """Create MicroRNA-Target Interaction Prediction dataloader object"""
        super().__init__(name,
                         path,
                         label_name,
                         print_stats,
                         dataset_names=dataset_names["MTI"])
        self.entity1_name = "miRNA"
        self.entity2_name = "Target"
        self.two_types = True

        if print_stats:
            self.print_stats()

        print("Done!", flush=True, file=sys.stderr)
