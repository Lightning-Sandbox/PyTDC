# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

from tdc.multi_pred import DTI
from tdc.multi_pred import DrugSyn
## requires RDKit
from tdc.single_pred import ADME


class TestFunctions:

    def test_random_split(self, tmp_path):
        data = ADME(name="Caco2_Wang", path=str(tmp_path))
        data.get_split(method="random")

    def test_scaffold_split(self, tmp_path):
        data = ADME(name="Caco2_Wang", path=str(tmp_path))
        data.get_split(method="scaffold")

    def test_cold_start_split(self, tmp_path):
        data = DTI(name="DAVIS", path=str(tmp_path))
        split = data.get_split(method="cold_split", column_name="Drug")

        set_train = set(split["train"]["Drug"])
        set_valid = set(split["valid"]["Drug"])
        set_test = set(split["test"]["Drug"])
        assert len(set_train.intersection(set_test)) == 0
        assert len(set_valid.intersection(set_test)) == 0
        assert len(set_train.intersection(set_valid)) == 0

        multi_split = data.get_split(method="cold_split",
                                     column_name=["Drug_ID", "Target_ID"])
        for entity in ["Drug_ID", "Target_ID"]:
            train_entity = set(multi_split["train"][entity])
            valid_entity = set(multi_split["valid"][entity])
            test_entity = set(multi_split["test"][entity])
            assert 0 == len(train_entity.intersection(valid_entity))
            assert 0 == len(train_entity.intersection(test_entity))
            assert 0 == len(valid_entity.intersection(test_entity))

    def test_combination_split(self, tmp_path):
        data = DrugSyn(name="DrugComb", path=str(tmp_path))
        data.get_split(method="combination")

    def test_time_split(self, tmp_path):
        data = DTI(name="BindingDB_Patent", path=str(tmp_path))
        data.get_split(method="time", time_column="Year")
