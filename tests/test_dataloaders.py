# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import os
import shutil
import unittest

import pandas as pd
from pandas import DataFrame

from tdc.generation import MolGen
from tdc.multi_pred import ProteinPeptide
from tdc.multi_pred import TestMultiPred
from tdc.multi_pred.perturboutcome import PerturbOutcome
from tdc.multi_pred.single_cell import CellXGene
from tdc.resource.dataloader import DataLoader
from tdc.single_pred import TestSinglePred
from tdc.single_pred.mpc import MPC

# TODO: add verification for the generation other than simple integration


class TestDataloader(unittest.TestCase):

    def setUp(self):
        print(os.getcwd())
        pass

    def test_single_pred(self, tmpdir):
        data = TestSinglePred(name="Test_Single_Pred", path=str(tmpdir))
        _ = data.get_split()

    def test_multi_pred(self, tmpdir):
        data = TestMultiPred(name="Test_Multi_Pred", path=str(tmpdir))
        _ = data.get_split()

    def test_resource_dataloader(self, tmpdir):
        dataloader = CellXGene(name="Tabula Sapiens - All Cells", path=str(tmpdir))
        gen = dataloader.get_data(
            value_filter="tissue == 'brain' and sex == 'male'")
        df = next(gen)
        assert isinstance(df, DataFrame)
        assert len(df) > 0
        print(df.head())
        # TODO: get_split() taking up too much memory...
        # split = dataloader.get_split(value_filter="tissue == 'brain' and sex == 'male'", debug=True)
        # assert "train" in split
        # assert isinstance(split["train"], DataFrame)
        # assert len(split["train"]) > 0
        # assert "test" in split
        # assert isinstance(split["test"], DataFrame)
        # assert len(split["test"]) > 0

    def test_cellxgene_list(self, tmpdir):
        dataloader = CellXGene(
            name=["Tabula Sapiens - Skin", "Tabula Sapiens - Kidney"],
            path=str(tmpdir)
        )
        gen = dataloader.get_data(
            value_filter="tissue == 'liver' and sex == 'male'")
        df = next(gen)
        assert isinstance(df, DataFrame)
        assert len(df) > 0
        print(df.head())

    def test_brown(self, tmpdir):
        # TODO: factor out into specialized test suites for individual datasets
        # this test serves as an integration test of the data processing, data configs, and existing tdc pipeline. leave here for now.
        data = ProteinPeptide(name="brown_mdm2_ace2_12ca5", path=str(tmpdir))
        assert "protein_or_rna_sequence" in data.get_data(
        ).columns  # brown protein<>peptide dataset uses a data config inserting this column
        data.get_split()

    @unittest.skip(
        "test is taking up too much memory"
    )  #FIXME: should probably create much smaller version and use that for the test. This test does pass locally, please rerun if changing anndata code.
    def test_h5ad_dataloader(self, tmpdir):
        test_loader = PerturbOutcome(name="scperturb_drug_AissaBenevolenskaya2021", path=str(tmpdir))
        testdf = test_loader.get_data()
        assert isinstance(testdf, DataFrame)
        test_loader.get_split()

    def test_generation(self, tmpdir):
        data = MolGen(name="ZINC", path=str(tmpdir))
        data.get_split()

    def test_resource_dataverse_dataloader(self, tmpdir):
        data = DataLoader(name="opentargets_dti", path=str(tmpdir))
        df = data.get_data()
        assert "Y" in df.columns
        split = data.get_split()
        assert "train" in split
        assert len(split["train"]) > 0
        assert len(split["test"]) > 0
        assert isinstance(split["train"], pd.DataFrame)

    def test_resource_dataverse_dataloader_raw_splits(self, tmpdir):
        data = DataLoader(name="tchard", path=str(tmpdir))
        df = data.get_data()
        assert isinstance(df, pd.DataFrame)
        assert "Y" in df.columns
        assert "splits" in data
        splits = data.get_split()
        assert "train" in splits
        assert "dev" in splits
        assert "test" in splits
        assert isinstance(
            splits["train"]["tchard_pep_cdr3b_only_neg_assays"][0],
            pd.DataFrame)
        assert isinstance(splits["test"]["tchard_pep_cdr3b_only_neg_assays"][2],
                          pd.DataFrame)
        assert not splits["dev"]

    def test_mpc(self, tmpdir):
        Xs = MPC(
            name="https://raw.githubusercontent.com/bidd-group/MPCD/main/dataset/ADMET/DeepDelta_benchmark/Caco2.csv",
            path=str(tmpdir)
        )
        Xs_split = Xs.get_split()
        Xs_train = Xs_split["train"]
        Xs_test = Xs_split["test"]
        _ = Xs_train["Y"]
        _ = Xs_test["Y"]
