import pytest
import numpy as np
from nabu.testutils import utilstest
from nabu.resources.dataset_analyzer import HDF5DatasetAnalyzer
from nabu.pipeline.estimators import CompositeCOREstimator


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls

    dataset_downloaded_path = utilstest.getfile("test_composite_cor_finder_data.h5")
    cls.theta_interval = 4.5 * 1  # this is given. Radios in the middle of steps 4.5 degree long
    # are set to zero for compression
    # You can still change it to a multiple of 4.5
    cls.cor_pix = 1321.625
    cls.abs_tol = 0.0001
    cls.dataset_info = HDF5DatasetAnalyzer(dataset_downloaded_path)
    cls.cor_options = """side="near"; near_pos = 300.0;  near_width = 20.0 """


@pytest.mark.usefixtures("bootstrap")
class TestCompositeCorFinder:
    def test(self):
        cor_finder = CompositeCOREstimator(
            self.dataset_info, theta_interval=self.theta_interval, cor_options=self.cor_options
        )

        cor_position = cor_finder.find_cor()
        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.cor_pix
        assert np.isclose(self.cor_pix, cor_position, atol=self.abs_tol), message
