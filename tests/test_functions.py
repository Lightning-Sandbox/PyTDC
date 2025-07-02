# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import unittest

from tdc import Evaluator
from tdc.single_pred import TestSinglePred


class TestFunctions(unittest.TestCase):

    def test_Evaluator(self):
        evaluator = Evaluator(name="ROC-AUC")
        print(evaluator([0, 1], [0.5, 0.6]))

    def test_binarize(self, tmp_path):
        data = TestSinglePred(name="Test_Single_Pred", path=str(tmp_path))
        data.binarize(threshold=-5, order="descending")

    def test_convert_to_log(self, tmp_path):
        data = TestSinglePred(name="Test_Single_Pred", path=str(tmp_path))
        data.convert_to_log()

    def test_print_stats(self, tmp_path):
        data = TestSinglePred(name="Test_Single_Pred", path=str(tmp_path))
        data.print_stats()
