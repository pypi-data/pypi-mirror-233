import numpy as np
from ..utils import get_opencl_srcfile, updiv, check_supported
from .kernel import OpenCLKernel
from .processing import OpenCLProcessing
from .memcpy import OpenCLMemcpy2D
import pyopencl.array as parray
from ..misc.padding_base import PaddingBase


class OpenCLPadding(PaddingBase):
    """
    A class for performing padding on GPU using Cuda
    """

    # TODO docstring from base class
    def __init__(self, shape, pad_width, mode="constant", opencl_options=None, **kwargs):
        super().__init__(shape, pad_width, mode=mode, **kwargs)
        self.opencl_processing = OpenCLProcessing(**(opencl_options or {}))
        self.queue = self.opencl_processing.queue
        self._init_opencl_coordinate_transform()

    def _init_opencl_coordinate_transform(self):
        if self.mode == "constant":
            self.d_padded_array_constant = parray.to_device(self.queue, self.padded_array_constant)
            self.memcpy2D = OpenCLMemcpy2D(ctx=self.opencl_processing.ctx, queue=self.queue)
            return
        self._coords_transform_kernel = OpenCLKernel(
            "coordinate_transform",
            self.opencl_processing.ctx,
            filename=get_opencl_srcfile("padding.cl"),
        )
        self._coords_transform_global_size = self.padded_shape[::-1]
        self.d_coords_rows = parray.to_device(self.queue, self.coords_rows)
        self.d_coords_cols = parray.to_device(self.queue, self.coords_cols)

    def _pad_constant(self, image, output):
        pad_y, pad_x = self.pad_width
        # the following line is not implemented in pyopencl
        # self.d_padded_array_constant[pad_y[0] : pad_y[0] + self.shape[0], pad_x[0] : pad_x[0] + self.shape[1]] = image[:]
        # cl.enqueue_copy is too cumbersome to use for Buffer <-> Buffer.
        # Use a dedicated kernel instead.
        # This is not optimal (two copies) - TODO write a constant padding kernel
        self.memcpy2D(self.d_padded_array_constant, image, image.shape[::-1], dst_offset_xy=(pad_x[0], pad_y[0]))
        output[:] = self.d_padded_array_constant[:]
        return output

    def pad(self, image, output=None):
        """
        Pad an array.

        Parameters
        ----------
        image: pycuda.gpuarray.GPUArray
            Image to pad
        output: pycuda.gpuarray.GPUArray, optional
            Output image. If provided, must be in the expected shape.
        """
        if output is None:
            output = self.opencl_processing.allocate_array("d_output", self.padded_shape)
        if self.mode == "constant":
            return self._pad_constant(image, output)
        self._coords_transform_kernel(
            self.queue,
            image,
            output,
            self.d_coords_cols,
            self.d_coords_rows,
            np.int32(self.shape[1]),
            np.int32(self.padded_shape[1]),
            np.int32(self.padded_shape[0]),
            global_size=self._coords_transform_global_size,
        )
        return output
