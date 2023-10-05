import numpy as np
import pytest
from nabu.opencl.utils import __has_pyopencl__, get_opencl_context
from nabu.utils import calc_padding_lengths, get_opencl_srcfile
from nabu.testutils import get_data, generate_tests_scenarios

if __has_pyopencl__:
    import pyopencl.array as parray
    from nabu.opencl.kernel import OpenCLKernel
    from nabu.opencl.padding import OpenCLPadding


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
    cls.data = get_data("brain_phantom.npz")["data"]
    cls.tol = 1e-7
    cls.ctx = get_opencl_context("all")
    yield


@pytest.mark.skipif(not (__has_pyopencl__), reason="Need OpenCL and pyopencl for this test")
@pytest.mark.usefixtures("bootstrap")
class TestOpenCLPadding:
    @pytest.mark.parametrize("config", scenarios)
    def test_padding(self, config):
        shape = config["shape"]
        data = self.data[: shape[0], : shape[1]]
        kwargs = {}
        if config["mode"] == "constant":
            kwargs["constant_values"] = config["constant_values"]
        ref = np.pad(data, config["pad_width"], mode=config["mode"], **kwargs)
        opencl_padding = OpenCLPadding(
            config["shape"],
            config["pad_width"],
            mode=config["mode"],
            constant_values=config["constant_values"],
            opencl_options={"ctx": self.ctx},
        )
        queue = opencl_padding.queue
        d_img = parray.to_device(queue, np.ascontiguousarray(data, dtype="f"))
        if config["output_is_none"]:
            output = None
        else:
            output = parray.zeros(queue, ref.shape, "f")
        res = opencl_padding.pad(d_img, output=output)

        err_max = np.max(np.abs(res.get() - ref))
        assert err_max < self.tol, str("Something wrong with padding for configuration %s" % (str(config)))

    def test_custom_coordinate_transform(self):
        data = self.data
        R, C = np.indices(data.shape, dtype=np.int32)

        pad_width = ((256, 255), (254, 251))
        mode = "reflect"

        coords_R = np.pad(R, pad_width, mode=mode)
        coords_C = np.pad(C, pad_width, mode=mode)
        # Further transform of coordinates - here FFT layout
        coords_R = np.roll(coords_R, (-pad_width[0][0], -pad_width[1][0]), axis=(0, 1))
        coords_C = np.roll(coords_C, (-pad_width[0][0], -pad_width[1][0]), axis=(0, 1))

        opencl_padding = OpenCLPadding(data.shape, (coords_R, coords_C), mode=mode, opencl_options={"ctx": self.ctx})
        queue = opencl_padding.queue
        d_img = parray.to_device(queue, data)
        d_out = parray.zeros(queue, opencl_padding.padded_shape, "f")
        res = opencl_padding.pad(d_img, output=d_out)

        ref = np.roll(np.pad(data, pad_width, mode=mode), (-pad_width[0][0], -pad_width[1][0]), axis=(0, 1))

        err_max = np.max(np.abs(d_out.get() - ref))
        assert err_max < self.tol, "Something wrong with custom padding"
