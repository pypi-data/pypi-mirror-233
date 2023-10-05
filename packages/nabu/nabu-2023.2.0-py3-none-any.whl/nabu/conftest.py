import pytest
from tomoscan.test.utils import HDF5MockContext


@pytest.fixture(scope="function")
def hdf5_scan(tmp_path):
    """simple fixture to create a scan and provide it to another function"""
    test_dir = tmp_path / "my_hdf5_scan"
    with HDF5MockContext(
        scan_path=str(test_dir),
        n_proj=10,
        n_ini_proj=10,
    ) as scan:
        yield scan
