# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

from tdc.chem_utils import MolFilter


def test_MolConvert(self):
    filters = MolFilter(filters=["PAINS"], HBD=[0, 6])
    filters(["CCSc1ccccc1C(=O)Nc1onc2c1CCC2"])
