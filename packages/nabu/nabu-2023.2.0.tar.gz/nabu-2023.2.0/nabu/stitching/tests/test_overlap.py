from nabu.stitching.overlap import compute_image_minimum_divergence, compute_image_higher_signal
from nabu.testutils import get_data
import numpy


def test_compute_image_minimum_divergence():
    """make sure the compute_image_minimum_divergence function is processing"""
    raw_data_1 = get_data("brain_phantom.npz")["data"]
    raw_data_2 = numpy.random.rand(*raw_data_1.shape) * 255.0

    stitching = compute_image_minimum_divergence(raw_data_1, raw_data_2, high_frequency_threshold=2)
    assert stitching.shape == raw_data_1.shape


def test_compute_image_higher_signal():
    """
    make sure compute_image_higher_signal is processing
    """
    raw_data = get_data("brain_phantom.npz")["data"]
    raw_data_1 = raw_data.copy()
    raw_data_1[40:75] = 0.0
    raw_data_1[:, 210:245] = 0.0

    raw_data_2 = raw_data.copy()
    raw_data_2[:, 100:120] = 0.0

    stitching = compute_image_higher_signal(raw_data_1, raw_data_2)

    numpy.testing.assert_array_equal(
        stitching,
        raw_data,
    )
