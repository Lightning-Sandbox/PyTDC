# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import os
import shutil
import unittest

from tdc.multi_pred import DDI
from tdc.multi_pred import DTI
from tdc.multi_pred import PPI
from tdc.single_pred import ADME
from tdc.single_pred import HTS
from tdc.utils import cid2smiles
from tdc.utils import get_label_map
from tdc.utils import uniprot2seq


class TestFunctions:

    def test_neg_sample(self, tmp_path):
        data = PPI(name="HuRI", path=str(tmp_path))
        data.neg_sample(frac=1)

    @unittest.skip("this is a visual test and should only be run locally")
    def test_label_distribution(self, tmp_path):
        data = ADME(name='Caco2_Wang', path=str(tmp_path))
        data.label_distribution()

    def test_get_label_map(self, tmp_path):
        data = DDI(name="DrugBank", path=str(tmp_path))
        data.get_split()
        get_label_map(name="DrugBank", task="DDI", path=str(tmp_path))

    def test_balanced(self, tmp_path):
        data = HTS(name="SARSCoV2_3CLPro_Diamond", path=str(tmp_path))
        data.balanced(oversample=True, seed=42)

    def test_cid2smiles(self):
        cid2smiles(2248631)

    def test_uniprot2seq(self):
        uniprot2seq("P49122")

    # note - this test might fail locally
    def test_to_graph(self, tmp_path):
        data = DTI(name="DAVIS", path=str(tmp_path))
        data.to_graph(
            threshold=30,
            format="edge_list",
            split=True,
            frac=[0.7, 0.1, 0.2],
            seed=42,
            order="descending",
        )
        # output: {'edge_list': array of shape (X, 2), 'neg_edges': array of shape (X, 2), 'split': {'train': df, 'valid': df, 'test': df}}
        data.to_graph(
            threshold=30,
            format="dgl",
            split=True,
            frac=[0.7, 0.1, 0.2],
            seed=42,
            order="descending",
        )
        # output: {'dgl_graph': the DGL graph object, 'index_to_entities': a dict map from ID in the data to node ID in the DGL object, 'split': {'train': df, 'valid': df, 'test': df}}

        data.to_graph(
            threshold=30,
            format="pyg",
            split=True,
            frac=[0.7, 0.1, 0.2],
            seed=42,
            order="descending",
        )
        # output: {'pyg_graph': the PyG graph object, 'index_to_entities': a dict map from ID in the data to node ID in the PyG object, 'split': {'train': df, 'valid': df, 'test': df}}
