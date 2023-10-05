from nabu.stitching.utils import shift_grid_search, ScoreMethod, has_itk, find_shift_with_itk
import scipy.misc
from scipy.ndimage import shift as scipy_shift
from scipy.ndimage import shift as shift_scipy
import numpy
import pytest


@pytest.mark.parametrize("shift", [(0, 3), (-4, 0), (8, -6)])
def test_shift_grid_search(shift):
    """
    test shift_grid_search algorithm
    """
    y = numpy.sin(numpy.linspace(0, numpy.pi, 250))

    weights = numpy.cos(numpy.linspace(-numpy.pi, numpy.pi, 120))
    image = numpy.outer(y, weights)
    # add a simple line with different value to ease detection
    image[150] = 1.0
    image[:, 50] = 1.2

    image_ref = image
    image_with_shift = scipy_shift(image_ref.copy(), shift=-numpy.array(shift))
    score_method = ScoreMethod.TV

    best_shift = shift_grid_search(
        image_ref,
        image_with_shift,
        window_sizes=(40, 20),
        axis=(0, 1),
        step_size=1,
        score_method=score_method,
    )

    assert tuple(best_shift) == shift


@pytest.mark.parametrize("data_type", (numpy.float32, numpy.uint16))
@pytest.mark.skipif(not has_itk, reason="itk not installed")
def test_find_shift_with_itk(data_type):
    shift = (5, 2)
    img1 = scipy.misc.ascent().astype(data_type)
    img2 = shift_scipy(
        img1.copy(),
        shift=shift,
        order=1,
    )

    img1 = img1[10:-10, 10:-10]
    img2 = img2[10:-10, 10:-10]
    assert find_shift_with_itk(img1=img1, img2=img2) == shift
