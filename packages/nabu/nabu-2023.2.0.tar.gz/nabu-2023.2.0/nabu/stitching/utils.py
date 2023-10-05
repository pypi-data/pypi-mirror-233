from distutils.version import StrictVersion

from typing import Optional, Union
import logging
import numpy
from tomoscan.scanbase import TomoScanBase
from nabu.misc import fourier_filters
from nabu.stitching.overlap import OverlapStitchingStrategy, ZStichOverlapKernel
from nabu.estimation.alignment import AlignmentBase
from nabu.resources.dataset_analyzer import HDF5DatasetAnalyzer
from silx.utils.enum import Enum as _Enum
from scipy.ndimage import shift as scipy_shift
from scipy.fft import rfftn as local_fftn
from scipy.fft import irfftn as local_ifftn
from nabu.resources.nxflatfield import update_dataset_info_flats_darks

try:
    import itk
except ImportError:
    has_itk = False
else:
    has_itk = True

_logger = logging.getLogger(__name__)


try:
    from skimage.registration import phase_cross_correlation
except ImportError:
    _logger.warning(
        "Unable to load skimage. Please install it if you want to use it for finding shifts from `find_relative_shifts`"
    )
    __has_sk_phase_correlation__ = False
else:
    __has_sk_phase_correlation__ = True


class ShiftAlgorithm(_Enum):
    """All generic shift search algorithm"""

    NABU_FFT = "nabu-fft"
    SKIMAGE = "skimage"
    SHIFT_GRID = "shift-grid"
    ITK_IMG_REG_V4 = "itk-img-reg-v4"
    NONE = "None"

    # In the case of shift search on radio along axis 2 (or axis x in image space) we can benefit from the existing
    # nabu algorithm such as growing-window or sliding-window
    CENTERED = "centered"
    GLOBAL = "global"
    SLIDING_WINDOW = "sliding-window"
    GROWING_WINDOW = "growing-window"
    SINO_COARSE_TO_FINE = "sino-coarse-to-fine"
    COMPOSITE_COARSE_TO_FINE = "composite-coarse-to-fine"

    @classmethod
    def from_value(cls, value):
        if value in ("", None):
            return ShiftAlgorithm.NONE
        else:
            return super().from_value(value=value)


def test_overlap_stitching_strategy(overlap_1, overlap_2, stitching_strategies):
    """
    stitch the two ovrelap with all the requested strategies.
    Return a dictionary with stitching strategy as key and a result dict as value.
    result dict keys are: 'weights_overlap_1', 'weights_overlap_2', 'stiching'
    """
    res = {}
    for strategy in stitching_strategies:
        s = OverlapStitchingStrategy.from_value(strategy)
        stitcher = ZStichOverlapKernel(
            stitching_strategy=s,
            frame_width=overlap_1.shape[1],
        )
        stiched_overlap, w1, w2 = stitcher.stitch(overlap_1, overlap_2, check_input=True)
        res[s.value] = {
            "stitching": stiched_overlap,
            "weights_overlap_1": w1,
            "weights_overlap_2": w2,
        }
    return res


def find_frame_relative_shifts(
    overlap_upper_frame: numpy.ndarray,
    overlap_lower_frame: numpy.ndarray,
    estimated_shifts,
    x_cross_correlation_function=None,
    y_cross_correlation_function=None,
    x_shifts_params: Optional[dict] = None,
    y_shifts_params: Optional[dict] = None,
):
    from nabu.stitching.config import (
        KEY_WINDOW_SIZE,
        KEY_SCORE_METHOD,
        KEY_LOW_PASS_FILTER,
        KEY_HIGH_PASS_FILTER,
    )  # avoid cyclic import

    x_cross_correlation_function = ShiftAlgorithm.from_value(x_cross_correlation_function)
    y_cross_correlation_function = ShiftAlgorithm.from_value(y_cross_correlation_function)

    if x_shifts_params is None:
        x_shifts_params = {}

    if y_shifts_params is None:
        y_shifts_params = {}

    # apply filtering if any
    def _str_to_int(value):
        if isinstance(value, str):
            value = value.lstrip("'").lstrip('"')
            value = value.rstrip("'").rstrip('"')
            value = int(value)
        return value

    low_pass = _str_to_int(x_shifts_params.get(KEY_LOW_PASS_FILTER, y_shifts_params.get(KEY_LOW_PASS_FILTER, None)))
    high_pass = _str_to_int(x_shifts_params.get(KEY_HIGH_PASS_FILTER, y_shifts_params.get(KEY_HIGH_PASS_FILTER, None)))
    if high_pass is None and low_pass is None:
        pass
    else:
        if low_pass is None:
            low_pass = 1
        if high_pass is None:
            high_pass = 20
        _logger.info(f"filter image for shift search (low_pass={low_pass}, high_pass={high_pass})")
        img_filter = fourier_filters.get_bandpass_filter(
            overlap_upper_frame.shape[-2:],
            cutoff_lowpass=low_pass,
            cutoff_highpass=high_pass,
            use_rfft=True,
            data_type=overlap_upper_frame.dtype,
        )
        overlap_upper_frame = local_ifftn(
            local_fftn(overlap_upper_frame, axes=(-2, -1)) * img_filter, axes=(-2, -1)
        ).real
        overlap_lower_frame = local_ifftn(
            local_fftn(overlap_lower_frame, axes=(-2, -1)) * img_filter, axes=(-2, -1)
        ).real

    # compute shifts
    initial_shifts = numpy.array(estimated_shifts).copy()
    extra_shifts = numpy.array([0.0, 0.0])

    # 2.0 call cross correlation function from the estimated cor from motors
    for axis, method, params in zip(
        (0, 1),
        (y_cross_correlation_function, x_cross_correlation_function),
        (y_shifts_params, x_shifts_params),
    ):
        if method is ShiftAlgorithm.NABU_FFT:
            extra_shifts[axis] = find_shift_correlate(img1=overlap_upper_frame, img2=overlap_lower_frame)[axis]
        elif method is ShiftAlgorithm.SKIMAGE:
            if not __has_sk_phase_correlation__:
                raise ValueError("scikit-image not installed. Cannot do phase correlation from it")
            else:
                found_shift, _, _ = phase_cross_correlation(
                    reference_image=overlap_upper_frame, moving_image=overlap_lower_frame, space="real"
                )
                extra_shifts[axis] = found_shift[axis]
        elif method is ShiftAlgorithm.NONE:  # None as a string in case some uers give this value
            # in the case we don't want to apply algorithm keep the initial 'guessed' shifts
            continue
        elif method is ShiftAlgorithm.SHIFT_GRID:
            if axis == 0:
                window_size = (int(y_shifts_params.get(KEY_WINDOW_SIZE, 200)), 0)
            elif axis == 1:
                window_size = (0, int(x_shifts_params.get(KEY_WINDOW_SIZE, 200)))
            score_method = params.get(KEY_SCORE_METHOD, ScoreMethod.STD)
            extra_shifts[axis] = -shift_grid_search(
                img_1=overlap_upper_frame,
                img_2=overlap_lower_frame,
                window_sizes=window_size,
                step_size=1,
                axis=(axis,),
                score_method=score_method,
            )[axis]
        elif method is ShiftAlgorithm.ITK_IMG_REG_V4:
            extra_shifts[axis] = find_shift_with_itk(img1=overlap_upper_frame, img2=overlap_lower_frame)[axis]
        else:
            raise ValueError(f"requested cross correlation function not handled ({method})")
    final_rel_shifts = numpy.array(extra_shifts) + initial_shifts

    return tuple([int(shift) for shift in final_rel_shifts])


def find_volumes_relative_shifts(
    upper_volume: numpy.ndarray,
    lower_volume: numpy.ndarray,
    estimated_shifts,
    flip_ud_upper_frame: bool = False,
    flip_ud_lower_frame: bool = False,
    slice_for_shift: Union[int, str] = "middle",
    x_cross_correlation_function=None,
    y_cross_correlation_function=None,
    x_shifts_params: Optional[dict] = None,
    y_shifts_params: Optional[dict] = None,
):
    if y_shifts_params is None:
        y_shifts_params = {}

    if x_shifts_params is None:
        x_shifts_params = {}

    upper_frame = upper_volume.get_slice(slice_for_shift, axis=1)
    lower_frame = lower_volume.get_slice(slice_for_shift, axis=1)
    if flip_ud_upper_frame:
        upper_frame = numpy.flipud(upper_frame.copy())
    if flip_ud_lower_frame:
        lower_frame = numpy.flipud(lower_frame.copy())

    from nabu.stitching.config import KEY_WINDOW_SIZE  # avoid cyclic import

    w_window_size = int(y_shifts_params.get(KEY_WINDOW_SIZE, 400))
    start_overlap = max(estimated_shifts[0] - w_window_size // 2, 0)
    end_overlap = min(estimated_shifts[0] + w_window_size // 2, min(upper_frame.shape[0], lower_frame.shape[0]))

    if start_overlap == 0:
        overlap_upper_frame = upper_frame[-end_overlap:]
    else:
        overlap_upper_frame = upper_frame[-end_overlap:-start_overlap]
    overlap_lower_frame = lower_frame[start_overlap:end_overlap]
    if not overlap_upper_frame.shape == overlap_lower_frame.shape:
        raise ValueError(f"Fail to get consistant overlap ({overlap_upper_frame.shape} vs {overlap_lower_frame.shape})")

    return find_frame_relative_shifts(
        overlap_upper_frame=overlap_upper_frame,
        overlap_lower_frame=overlap_lower_frame,
        estimated_shifts=estimated_shifts,
        x_cross_correlation_function=x_cross_correlation_function,
        y_cross_correlation_function=y_cross_correlation_function,
        x_shifts_params=x_shifts_params,
        y_shifts_params=y_shifts_params,
    )


from nabu.pipeline.estimators import estimate_cor


def find_projections_relative_shifts(
    upper_scan: TomoScanBase,
    lower_scan: TomoScanBase,
    estimated_shifts,
    flip_ud_upper_frame: bool = False,
    flip_ud_lower_frame: bool = False,
    projection_for_shift: Union[int, str] = "middle",
    invert_order: bool = False,
    x_cross_correlation_function=None,
    y_cross_correlation_function=None,
    x_shifts_params: Optional[dict] = None,
    y_shifts_params: Optional[dict] = None,
) -> tuple:
    """
    deduce the relative shift between the two scans.
    Expected behavior:
    * compute expected overlap area from z_translations and (sample) pixel size
    * call an (optional) cross correlation function from the overlap area to compute the x shift and polish the y shift from `projection_for_shift`

    :param TomoScanBase scan_0:
    :param TomoScanBase scan_1:
    :param int axis_0_overlap_px: overlap between the two scans in pixel
    :param Union[int,str] projection_for_shift: index fo the projection to use (in projection space or in scan space ?. For now in projection) or str. If str must be in (`middle`, `first`, `last`)
    :param str x_cross_correlation_function: optional method to refine x shift from computing cross correlation. For now valid values are: ("skimage", "nabu-fft")
    :param str y_cross_correlation_function: optional method to refine y shift from computing cross correlation. For now valid values are: ("skimage", "nabu-fft")
    :param int minimal_overlap_area_for_cross_correlation: if first approximated overlap shift found from z_translation is lower than this value will fall back on taking the full image for the cross correlation and log a warning
    :param bool invert_order: are projections inverted between the two scans (case if rotation angle are inverted)
    :param tuple estimated_shifts: 'a priori' shift estimation
    :return: relative shift of scan_1 with scan_0 as reference: (y_shift, x_shift)
    :rtype: tuple

    :warning: this function will flip left-right and up-down frames by default. So it will return shift according to this information
    """
    if x_shifts_params is None:
        x_shifts_params = {}
    if y_shifts_params is None:
        y_shifts_params = {}
    if estimated_shifts[0] < 0:
        raise ValueError("y_overlap_px is expected to be stricktly positive")

    x_cross_correlation_function = ShiftAlgorithm.from_value(x_cross_correlation_function)
    y_cross_correlation_function = ShiftAlgorithm.from_value(y_cross_correlation_function)

    # { handle specific use case (finding shift on scan) - when using nabu COR algorithms (for axis 2)
    if x_cross_correlation_function in (
        ShiftAlgorithm.SINO_COARSE_TO_FINE,
        ShiftAlgorithm.COMPOSITE_COARSE_TO_FINE,
        ShiftAlgorithm.CENTERED,
        ShiftAlgorithm.GLOBAL,
        ShiftAlgorithm.GROWING_WINDOW,
        ShiftAlgorithm.SLIDING_WINDOW,
    ):
        cor_options = x_shifts_params.copy()
        cor_options.pop("img_reg_method", None)
        cor_options.pop("score_method", None)
        # remove all none numeric options because estimate_cor will call 'literal_eval' on them

        upper_scan_dataset_info = HDF5DatasetAnalyzer(
            location=upper_scan.master_file, extra_options={"hdf5_entry": upper_scan.entry}
        )
        update_dataset_info_flats_darks(upper_scan_dataset_info, flatfield_mode=1)

        upper_scan_pos = estimate_cor(
            method=x_cross_correlation_function.value,
            dataset_info=upper_scan_dataset_info,
            cor_options=cor_options,
        )
        lower_scan_dataset_info = HDF5DatasetAnalyzer(
            location=lower_scan.master_file, extra_options={"hdf5_entry": lower_scan.entry}
        )
        update_dataset_info_flats_darks(lower_scan_dataset_info, flatfield_mode=1)
        lower_scan_pos = estimate_cor(
            method=x_cross_correlation_function.value,
            dataset_info=lower_scan_dataset_info,
            cor_options=cor_options,
        )

        estimated_shifts = tuple(
            [
                estimated_shifts[0],
                (lower_scan_pos - upper_scan_pos),
            ]
        )
        x_cross_correlation_function = ShiftAlgorithm.NONE

    # } else we will compute shift from the flat projections

    def get_flat_fielded_proj(scan: TomoScanBase, proj_index: int, reverse: bool, revert_x: bool, revert_y):
        first_proj_idx = sorted(lower_scan.projections.keys(), reverse=reverse)[proj_index]
        ff = scan.flat_field_correction(
            (scan.projections[first_proj_idx],),
            (first_proj_idx,),
        )[0]
        if revert_x:
            ff = numpy.fliplr(ff)
        if revert_y:
            ff = numpy.flipud(ff)
        return ff

    if isinstance(projection_for_shift, str):
        if projection_for_shift.lower() == "first":
            projection_for_shift = 0
        elif projection_for_shift.lower() == "last":
            projection_for_shift = -1
        elif projection_for_shift.lower() == "middle":
            projection_for_shift = len(upper_scan.projections) // 2
        else:
            try:
                projection_for_shift = int(projection_for_shift)
            except ValueError:
                raise ValueError(
                    f"{projection_for_shift} cannot be cast to an int and is not one of the possible ('first', 'last', 'middle')"
                )
    elif not isinstance(projection_for_shift, (int, numpy.number)):
        raise TypeError(
            f"projection_for_shift is expected to be an int. Not {type(projection_for_shift)} - {projection_for_shift}"
        )

    upper_proj = get_flat_fielded_proj(
        upper_scan,
        projection_for_shift,
        reverse=False,
        revert_x=upper_scan.get_x_flipped(default=False),
        revert_y=upper_scan.get_y_flipped(default=False) ^ flip_ud_upper_frame,
    )
    lower_proj = get_flat_fielded_proj(
        lower_scan,
        projection_for_shift,
        reverse=invert_order,
        revert_x=lower_scan.get_x_flipped(default=False),
        revert_y=lower_scan.get_y_flipped(default=False) ^ flip_ud_lower_frame,
    )

    from nabu.stitching.config import KEY_WINDOW_SIZE  # avoid cyclic import

    w_window_size = int(y_shifts_params.get(KEY_WINDOW_SIZE, 400))
    start_overlap = max(estimated_shifts[0] - w_window_size // 2, 0)
    end_overlap = min(estimated_shifts[0] + w_window_size // 2, min(upper_proj.shape[0], lower_proj.shape[0]))
    if start_overlap == 0:
        overlap_upper_frame = upper_proj[-end_overlap:]
    else:
        overlap_upper_frame = upper_proj[-end_overlap:-start_overlap]
    overlap_lower_frame = lower_proj[start_overlap:end_overlap]
    if not overlap_upper_frame.shape == overlap_lower_frame.shape:
        raise ValueError(f"Fail to get consistant overlap ({overlap_upper_frame.shape} vs {overlap_lower_frame.shape})")

    return find_frame_relative_shifts(
        overlap_upper_frame=overlap_upper_frame,
        overlap_lower_frame=overlap_lower_frame,
        estimated_shifts=estimated_shifts,
        x_cross_correlation_function=x_cross_correlation_function,
        y_cross_correlation_function=y_cross_correlation_function,
        x_shifts_params=x_shifts_params,
        y_shifts_params=y_shifts_params,
    )


def find_shift_correlate(img1, img2, padding_mode="reflect"):
    alignment = AlignmentBase()
    cc = alignment._compute_correlation_fft(
        img1,
        img2,
        padding_mode,
    )

    img_shape = img1.shape[-2:]
    cc_vs = numpy.fft.fftfreq(img_shape[-2], 1 / img_shape[-2])
    cc_hs = numpy.fft.fftfreq(img_shape[-1], 1 / img_shape[-1])

    (f_vals, fv, fh) = alignment.extract_peak_region_2d(cc, cc_vs=cc_vs, cc_hs=cc_hs)
    shifts_vh = alignment.refine_max_position_2d(f_vals, fv, fh)
    return shifts_vh


class ScoreMethod(_Enum):
    STD = "standard deviation"
    TV = "total variation"
    TV_INVERSE = "1 / (total variation)"
    STD_INVERSE = "1 / std"

    @classmethod
    def from_value(cls, value):
        if isinstance(value, str):
            # for string handle the case where value as been provided as 'value'. As there is spaces this can happen
            value = value.lstrip("'").rstrip("'")
        if value in ("tv", "TV"):
            return ScoreMethod.TV
        elif value in ("std", "STD"):
            return ScoreMethod.STD
        else:
            return super().from_value(value=value)


def compute_score_contrast_std(data: numpy.ndarray):
    """
    Compute a contrast score by simply computing the standard deviation of
    the frame
    :param numpy.ndarray data: frame for which we should compute the score
    :return: score of the frame
    :rtype: float
    """
    if data is None:
        return None
    else:
        return data.std()


def compute_tv_score(data: numpy.ndarray):
    """
    Compute the data score as image total variation

    :param numpy.ndarray data: frame for which we should compute the score
    :return: score of the frame
    :rtype: float
    """
    tv = numpy.sum(numpy.sqrt(numpy.gradient(data, axis=0) ** 2 + numpy.gradient(data, axis=1) ** 2))
    return tv


def compute_score(img_1, img_2, shift, score_method, score_region, return_img=False):
    score_method = ScoreMethod.from_value(score_method)

    img_2 = scipy_shift(img_2, shift=shift)

    img_2_reduce = img_2[
        score_region[0].start : score_region[0].stop,
        score_region[1].start : score_region[1].stop,
    ]
    img_1_reduce = img_1[
        score_region[0].start : score_region[0].stop,
        score_region[1].start : score_region[1].stop,
    ]

    img_sum = img_1_reduce * 0.5 + img_2_reduce * 0.5

    if score_method is ScoreMethod.TV:
        result = compute_tv_score(img_sum)
    elif score_method is ScoreMethod.STD:
        result = compute_score_contrast_std(img_sum)
    elif score_method is ScoreMethod.TV_INVERSE:
        result = 1 / compute_tv_score(img_sum)
    elif score_method is ScoreMethod.STD_INVERSE:
        result = 1 / compute_score_contrast_std(img_sum)
    else:
        raise ValueError(f"{score_method} is not handled")
    if return_img:
        return result, img_sum
    else:
        return result


def shift_grid_search(img_1, img_2, window_sizes: tuple, axis, step_size, score_method=ScoreMethod.STD):
    """
    we could consider adding weights to do the exact same operation that will be done for the stitching... ? overkilled ?
    :param tuple window_sizes: as y_size, x_size
    """
    if not isinstance(window_sizes, tuple) and len(window_sizes) != 2:
        raise TypeError(f"window_sizes is expected to be a tuple of two ints. {window_sizes} provided")
    if not img_1.ndim == img_2.ndim == 2:
        raise ValueError("image dimension should be 2D")

    for value in axis:
        if not value in (0, 1):
            raise ValueError(f"axis {value} is not handled")
    half_window_x = min((img_1.shape[1], img_2.shape[1], abs(window_sizes[1]))) // 2
    half_window_y = min((img_1.shape[0], img_2.shape[0], abs(window_sizes[0]))) // 2
    if 1 in axis:
        x_research = numpy.arange(-half_window_x, half_window_x, step_size)
        x_score_region = slice(
            int(half_window_x * 2),
            int(min(img_1.shape[1], img_2.shape[1]) - (half_window_x * 2)),
        )
    else:
        x_research = tuple((0,))
        x_score_region = slice(0, int(min(img_1.shape[1], img_2.shape[1])))

    if 0 in axis:
        y_research = numpy.arange(-half_window_y, half_window_y, step_size)
        y_score_region = slice(
            int((half_window_y * 2)),
            int(min(img_1.shape[0], img_2.shape[0]) - (half_window_y * 2)),
        )
    else:
        y_research = tuple((0,))
        y_score_region = slice(0, int(min(img_1.shape[0], img_2.shape[0])))
    score_region = (
        y_score_region,
        x_score_region,
    )

    score_width = score_region[1].stop - score_region[1].start
    if score_width < 10:
        _logger.warning("score_width seems very low. Try reducing window_sizes")

    best_score, best_shift = None, (0, 0)
    for x_shift in x_research:
        for y_shift in y_research:
            res = compute_score(
                img_1,
                img_2.copy(),
                shift=(y_shift, x_shift),
                score_method=score_method,
                score_region=score_region,
            )
            local_score = res
            if best_score is None or (local_score is not None and local_score > best_score):
                best_score = local_score
                best_shift = (y_shift, x_shift)
    return numpy.array(best_shift)


def find_shift_with_itk(img1: numpy.ndarray, img2: numpy.ndarray) -> tuple:
    # created from https://examples.itk.org/src/registration/common/perform2dtranslationregistrationwithmeansquares/documentation
    # return (y_shift, x_shift). For now shift are integers as only integer shift are handled.
    if not img1.dtype == img2.dtype:
        raise ValueError("the two images are expected to have the same type")
    if not img1.ndim == img2.ndim == 2:
        raise ValueError("the two images are expected to 2D numpy arrays")

    if not has_itk:
        _logger.warning("itk is not installed. Please install it to find shift with it")
        return (0, 0)

    if StrictVersion(itk.Version.GetITKVersion()) < StrictVersion("4.9.0"):
        _logger.error("ITK 4.9.0 is required to find shift with it.")
        return (0, 0)

    pixel_type = itk.ctype("float")
    img1 = numpy.ascontiguousarray(img1, dtype=numpy.float32)
    img2 = numpy.ascontiguousarray(img2, dtype=numpy.float32)

    dimension = 2
    image_type = itk.Image[pixel_type, dimension]

    fixed_image = itk.PyBuffer[image_type].GetImageFromArray(img1)
    moving_image = itk.PyBuffer[image_type].GetImageFromArray(img2)

    transform_type = itk.TranslationTransform[itk.D, dimension]
    initial_transform = transform_type.New()

    optimizer = itk.RegularStepGradientDescentOptimizerv4.New(
        LearningRate=4,
        MinimumStepLength=0.001,
        RelaxationFactor=0.5,
        NumberOfIterations=200,
    )

    metric = itk.MeanSquaresImageToImageMetricv4[image_type, image_type].New()

    registration = itk.ImageRegistrationMethodv4.New(
        FixedImage=fixed_image,
        MovingImage=moving_image,
        Metric=metric,
        Optimizer=optimizer,
        InitialTransform=initial_transform,
    )

    moving_initial_transform = transform_type.New()
    initial_parameters = moving_initial_transform.GetParameters()
    initial_parameters[0] = 0
    initial_parameters[1] = 0
    moving_initial_transform.SetParameters(initial_parameters)
    registration.SetMovingInitialTransform(moving_initial_transform)

    identity_transform = transform_type.New()
    identity_transform.SetIdentity()
    registration.SetFixedInitialTransform(identity_transform)

    registration.SetNumberOfLevels(1)
    registration.SetSmoothingSigmasPerLevel([0])
    registration.SetShrinkFactorsPerLevel([1])

    registration.Update()

    transform = registration.GetTransform()
    final_parameters = transform.GetParameters()
    translation_along_x = final_parameters.GetElement(0)
    translation_along_y = final_parameters.GetElement(1)

    return numpy.round(translation_along_y), numpy.round(translation_along_x)
