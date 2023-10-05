import numpy as np
from ..thirdparty.pore3d_deringer_munch import munchetal_filter
from ..utils import get_2D_3D_shape


class MunchDeringer:
    def __init__(self, sigma, sinos_shape, levels=None, wname="db15", padding=None, padding_mode="edge"):
        """
        Initialize a "Munch Et Al" sinogram deringer. See References for more information.

        Parameters
        -----------
        sigma: float
            Standard deviation of the damping parameter. The higher value of sigma,
            the more important the filtering effect on the rings.
        levels: int, optional
            Number of wavelets decomposition levels.
            By default (None), the maximum number of decomposition levels is used.
        wname: str, optional
            Default is "db15" (Daubechies, 15 vanishing moments)
        sinos_shape: tuple, optional
            Shape of the sinogram (or sinograms stack).
        padding: tuple of two int, optional
            Horizontal padding to use for reducing the aliasing artefacts

        References
        ----------
        B. Munch, P. Trtik, F. Marone, M. Stampanoni, Stripe and ring artifact removal with
        combined wavelet-Fourier filtering, Optics Express 17(10):8567-8591, 2009.
        """
        self._get_shapes(sinos_shape, padding)
        self.sigma = sigma
        self.levels = levels
        self.wname = wname
        self.padding_mode = padding_mode
        self._check_can_use_wavelets()

    def _get_shapes(self, sinos_shape, padding):
        n_z, n_a, n_x = get_2D_3D_shape(sinos_shape)
        self.sinos_shape = n_z, n_a, n_x
        self.n_angles = n_a
        self.n_z = n_z
        self.n_x = n_x
        # Handle "padding=True" or "padding=False"
        if isinstance(padding, bool):
            if padding:
                padding = (n_x // 2, n_x // 2)
            else:
                padding = None
        #
        if padding is not None:
            pad_x1, pad_x2 = padding
            if np.iterable(pad_x1) or np.iterable(pad_x2):
                raise ValueError("Expected padding in the form (x1, x2)")
            self.sino_padded_shape = (n_a, n_x + pad_x1 + pad_x2)
        self.padding = padding

    def _check_can_use_wavelets(self):
        if munchetal_filter is None:
            raise ValueError("Need pywavelets to use this class")

    def _destripe_2D(self, sino, output):
        if self.padding is not None:
            sino = np.pad(sino, ((0, 0), self.padding), mode=self.padding_mode)
        res = munchetal_filter(sino, self.levels, self.sigma, wname=self.wname)
        if self.padding is not None:
            res = res[:, self.padding[0] : -self.padding[1]]
        output[:] = res
        return output

    def remove_rings(self, sinos, output=None):
        """
        Main function to performs rings artefacts removal on sinogram(s).
        CAUTION: this function defaults to in-place processing, meaning that
        the sinogram(s) you pass will be overwritten.

        Parameters
        ----------
        sinos: numpy.ndarray
            Sinogram or stack of sinograms.
        output: numpy.ndarray, optional
            Output array. If set to None (default), the output overwrites the input.
        """
        if output is None:
            output = sinos
        if sinos.ndim == 2:
            return self._destripe_2D(sinos, output)
        n_sinos = sinos.shape[0]
        for i in range(n_sinos):
            self._destripe_2D(sinos[i], output[i])
        return output
