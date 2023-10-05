"""
import numpy as np
import pytest
from nabu.opencl.utils import __has_pyopencl__, get_opencl_context
from nabu.utils import calc_padding_lengths, get_opencl_srcfile
from nabu.testutils import get_data, generate_tests_scenarios, __do_long_tests__

if __has_pyopencl__:
    import pyopencl.array as parray
    from nabu.opencl.fftshift import OpenCLfftshift


scenarios = generate_tests_scenarios(
    {
        "shape": [(511, 512), (512, 511)],
        "pad_width": [((256, 255), (128, 127)), ((0, 0), (6, 7))],
        "mode": OpenCLPadding.supported_modes if __has_pyopencl__ else [],
        "constant_values": [0, ((1.0, 2.0), (3.0, 4.0))],
        "output_is_none": [True, False],
    }
)


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.data = get_data('brain_phantom.npz')['data']
    cls.tol = 1e-7
    cls.ctx = get_opencl_context("all")
    yield


@pytest.mark.skipif(not (__has_pyopencl__), reason="Need OpenCL and pyopencl for this test")
@pytest.mark.usefixtures("bootstrap")
class TestOpenCLFFTshift:
    @pytest.mark.parametrize("config", scenarios)
    def test_fftshift(self, config):
        direction = config["direction"]
        shape = config["shape"]
        dtype = config["dtype"]

        data = np.squeeze(self.data[: shape[0], : shape[1]]).astype(dtype)  # can be 1D or 2D

        shifter = OpenCLfftshift(data.shape, data.dtype, opencl_options={"ctx": self.ctx})
        queue = shifter.queue
        d_data = parray.to_device(queue, data)
        shifter(d_data)  # in-place
        res = d_data.get()

        reference_shifter = np.fft.fftshift if direction == "forward" else np.fft.ifftshift
        ref = reference_shifter(x, axes=config["axes"])

        err_max = np.max(np.abs(res - ref))
        assert err_max < self.tol, str("Something wrong with fftshift for configuration %s" % (str(config)))
"""
