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

    def test_binarize(self, tmpdir):
        data = TestSinglePred(name="Test_Single_Pred", path=str(tmpdir))
        data.binarize(threshold=-5, order="descending")

    def test_convert_to_log(self, tmpdir):
        data = TestSinglePred(name="Test_Single_Pred", path=str(tmpdir))
        data.convert_to_log()

    def test_print_stats(self, tmpdir):
        data = TestSinglePred(name="Test_Single_Pred", path=str(tmpdir))
        data.print_stats()
