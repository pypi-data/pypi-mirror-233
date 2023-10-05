import numpy as np
import pytest
from nabu.utils import clip_circle
from nabu.testutils import get_data, compare_arrays, generate_tests_scenarios, __do_long_tests__
from nabu.reconstruction.rings import MunchDeringer
from nabu.thirdparty.pore3d_deringer_munch import munchetal_filter
from nabu.cuda.utils import __has_pycuda__, get_cuda_context

__have_gpuderinger__ = False
if __has_pycuda__:
    import pycuda.gpuarray as garray
    from nabu.reconstruction.rings_cuda import CudaMunchDeringer, __have_pycudwt__, __have_skcuda__

    if __have_pycudwt__ and __have_skcuda__:
        __have_gpuderinger__ = True


fw_scenarios = generate_tests_scenarios(
    {
        "levels": [4],
        "sigma": [1.0],
        "wname": ["db15"],
        "padding": [None],
    }
)
if __do_long_tests__:
    fw_scenarios = generate_tests_scenarios(
        {
            "levels": [4, 2],
            "sigma": [1.0, 2.0],
            "wname": ["db15", "haar", "rbio4.4"],
            "padding": [None, (100, 100), (50, 71)],
        }
    )


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.sino = get_data("mri_sino500.npz")["data"]
    cls.tol = 5e-3
    cls.rings = {150: 0.5, -150: 0.5}
    if __have_gpuderinger__:
        cls.ctx = get_cuda_context(cleanup_at_exit=False)
    yield
    if __have_gpuderinger__:
        cls.ctx.pop()


@pytest.mark.usefixtures("bootstrap")
class TestMunchDeringer:
    @staticmethod
    def add_stripes_to_sino(sino, rings_desc):
        """
        Create a new sinogram by adding synthetic stripes to an existing one.

        Parameters
        ----------
        sino: array-like
            Sinogram.
        rings_desc: dict
            Dictionary describing the stripes locations and intensity.
            The location is an integer in [0, N[ where N is the number of columns.
            The intensity is a float: percentage of the current column mean value.
        """
        sino_out = np.copy(sino)
        for loc, intensity in rings_desc.items():
            sino_out[:, loc] += sino[:, loc].mean() * intensity
        return sino_out

    @staticmethod
    def get_fourier_wavelets_reference_result(sino, config):
        # Reference destriping with pore3d "munchetal_filter"
        padding = config.get("padding", None)
        if padding is not None:
            sino = np.pad(sino, ((0, 0), padding), mode="edge")
        ref = munchetal_filter(sino, config["levels"], config["sigma"], wname=config["wname"])
        if config["padding"] is not None:
            ref = ref[:, padding[0] : -padding[1]]
        return ref

    @pytest.mark.skipif(munchetal_filter is None, reason="Need PyWavelets for this test")
    @pytest.mark.parametrize("config", fw_scenarios)
    def test_munch_deringer(self, config):
        deringer = MunchDeringer(
            config["sigma"], self.sino.shape, levels=config["levels"], wname=config["wname"], padding=config["padding"]
        )
        sino = self.add_stripes_to_sino(self.sino, self.rings)
        ref = self.get_fourier_wavelets_reference_result(sino, config)
        # Wrapping with DeRinger
        res = np.zeros((1,) + sino.shape, dtype=np.float32)
        deringer.remove_rings(sino, output=res)

        err_max = np.max(np.abs(res[0] - ref))
        assert err_max < self.tol, "Max error is too high"

    @pytest.mark.skipif(
        not (__have_gpuderinger__) or munchetal_filter is None,
        reason="Need pycuda, pycudwt and scikit-cuda for this test",
    )
    @pytest.mark.parametrize("config", fw_scenarios)
    def test_cuda_munch_deringer(self, config):
        sino = self.add_stripes_to_sino(self.sino, self.rings)
        deringer = CudaMunchDeringer(
            config["sigma"],
            self.sino.shape,
            levels=config["levels"],
            wname=config["wname"],
            cuda_options={"ctx": self.ctx},
        )
        d_sino = garray.to_gpu(sino)
        deringer.remove_rings(d_sino)
        res = d_sino.get()

        ref = self.get_fourier_wavelets_reference_result(sino, config)

        err_max = np.max(np.abs(res - ref))
        assert err_max < 1e-1, "Max error is too high"
