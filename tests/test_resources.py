import os
import unittest

from pandas import DataFrame

from tdc.resource import PrimeKG
from tdc.resource import cellxgene_census
from tdc.resource.pharmone import PharmoneMap
from tdc.resource.pinnacle import PINNACLE


class TestCellXGene(unittest.TestCase):

    def setUp(self):
        self.resource = cellxgene_census.CensusResource()
        self.gene_value_filter = "feature_id in ['ENSG00000161798', 'ENSG00000188229']"
        self.gene_column_names = ["feature_name", "feature_length"]
        self.cell_value_filter = "tissue == 'brain' and sex == 'male'"
        self.cell_column_names = ["assay", "cell_type", "tissue"]
        print(os.getcwd())

    def test_get_cell_metadata(self):
        obsdf = self.resource.get_cell_metadata(
            value_filter=self.cell_value_filter,
            column_names=self.cell_column_names,
            fmt="pandas")
        assert isinstance(obsdf, DataFrame)

    def test_get_gene_metadata(self):
        varpyarrow = self.resource.get_gene_metadata(
            value_filter=self.gene_value_filter,
            column_names=self.gene_column_names,
            fmt="pyarrow",
            measurement_name="RNA")
        print(varpyarrow)

    def test_get_measurement_matrix(self):
        X = self.resource.query_measurement_matrix(
            measurement_name="RNA",
            fmt="pyarrow",
            value_adjustment="raw",
            value_filter="tissue == 'brain' and sex == 'male'")
        next(X)[:3]

    def test_get_feature_dataset_presence_matrix(self):
        FMslice = self.resource.get_feature_dataset_presence_matrix(
            upper=5,
            lower=0,
            measurement_name="RNA",
            fmt="pyarrow",
            todense=False)
        print("f", FMslice)


class TestPrimeKG(unittest.TestCase):

    def test_node_retrieval(self, tmpdir):
        data = PrimeKG(path=str(tmpdir))
        drug_feature = data.get_features(feature_type='drug')
        data.to_nx()
        l = data.get_node_list('disease')
        assert "1" in l and "9997" in l


class TestPINNACLE(unittest.TestCase):

    def test_mg_ppi_load(self, tmpdir):
        pinnacle = PINNACLE(path=str(tmpdir))
        assert isinstance(pinnacle.get_ppi(), DataFrame)
        assert isinstance(pinnacle.get_mg(), DataFrame)
        assert len(pinnacle.get_ppi()) > 0
        assert len(pinnacle.get_mg()) > 0
        embeds = pinnacle.get_embeds()
        assert isinstance(embeds, DataFrame)
        assert len(embeds) > 0, "PINNACLE embeds is empty"

    def test_embeddings(self, tmpdir):
        pinnacle = PINNACLE(path=str(tmpdir))
        embeds = pinnacle.get_embeds()
        assert isinstance(embeds, DataFrame)
        assert len(embeds) > 0, "PINNACLE embeds is empty"
        keys = pinnacle.get_keys()
        assert isinstance(keys, DataFrame)
        assert len(keys) > 0, "PINNACLE keys is empty"
        assert len(keys) == len(embeds), "{} vs {}".format(
            len(keys), len(embeds))
        num_targets = len(keys["target"].unique())
        num_cells = len(keys["cell type"].unique())
        all_entries = embeds.index
        prots = [x.split("--")[0] for x in all_entries]
        cells = [x.split("--")[1] for x in all_entries]
        assert len(
            set(prots)) == num_targets, "{} vs {} for target proteins".format(
                len(prots), num_targets)
        assert len(set(cells)) == num_cells, "{} vs {} for cell_types".format(
            len(cells), num_cells)

    def test_exp_data(self, tmpdir):
        pinnacle = PINNACLE(path=str(tmpdir))
        exp_data = pinnacle.get_exp_data()
        assert isinstance(exp_data, DataFrame)
        assert len(exp_data) > 0, "PINNACLE exp_data is empty"


class TestPharmoneMap(unittest.TestCase):

    def test_get_data(self, tmpdir):
        resource = PharmoneMap(path=str(tmpdir))
        data = resource.get_data()
        assert isinstance(data, DataFrame), type(data)
        assert "Compound" in data.columns
        assert "Target_ID" in data.columns
        assert "pXC50" in data.columns
