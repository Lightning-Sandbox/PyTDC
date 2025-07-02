# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import os
import shutil
import unittest

from tdc.chem_utils import MolConvert


class TestMolConvert(unittest.TestCase):

    def test_MolConvert(self):
        converter = MolConvert(src="SMILES", dst="Graph2D")
        converter([
            "Clc1ccccc1C2C(=C(/N/C(=C2/C(=O)OCC)COCCN)C)\C(=O)OC",
            "CCCOc1cc2ncnc(Nc3ccc4ncsc4c3)c2cc1S(=O)(=O)C(C)(C)C",
        ])

        MolConvert.eligible_format()

    def tearDown(self):
        print(os.getcwd())

        if os.path.exists(os.path.join(os.getcwd(), "data")):
            shutil.rmtree(os.path.join(os.getcwd(), "data"))
