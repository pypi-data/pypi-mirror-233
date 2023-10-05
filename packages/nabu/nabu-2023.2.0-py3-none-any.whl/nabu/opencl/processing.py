import numpy as np
from ..misc.processing_base import ProcessingBase
from .utils import get_opencl_context, __has_pyopencl__

if __has_pyopencl__:
    import pyopencl as cl
    import pyopencl.array as parray


class OpenCLProcessing(ProcessingBase):
    _array_class = parray.Array

    def __init__(self, ctx=None, device_type="all", queue=None, **kwargs):
        """
        Initialie a OpenCLProcessing instance.

        Parameters
        ----------
        ctx: pycuda.driver.Context, optional
            Existing context to use. If provided, do not create a new context.
        cleanup_at_exit: bool, optional
            Whether to clean-up the context at exit.
            Ignored if ctx is not None.
        """
        super().__init__()
        if queue is not None:
            # re-use an existing queue. In this case the this instance is mostly for convenience
            ctx = queue.context
        if ctx is None:
            self.ctx = get_opencl_context(device_type=device_type, **kwargs)
        else:
            self.ctx = ctx
        if queue is None:
            queue = cl.CommandQueue(self.ctx)
        self.queue = queue

    # TODO push_context, pop_context ?

    def _allocate_array_mem(self, shape, dtype):
        return parray.zeros(self.queue, shape, dtype)
