# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "10/05/2022"


from dataclasses import dataclass
import numpy
from tomoscan.identifier import VolumeIdentifier, ScanIdentifier
from tomoscan.esrf import HDF5TomoScan
from tomoscan.nexus.paths import nxtomo
from silx.utils.enum import Enum as _Enum
from typing import Optional, Union, Sized
from nabu.pipeline.config_validators import (
    integer_validator,
    list_of_shift_validator,
    list_of_tomoscan_identifier,
    optional_directory_location_validator,
    boolean_validator,
    convert_to_bool,
    optional_positive_integer_validator,
    output_file_format_validator,
    optional_tuple_of_floats_validator,
    optional_file_name_validator,
)
from nabu.stitching.overlap import OverlapStitchingStrategy
from nabu.utils import concatenate_dict, convert_str_to_tuple
from nabu.io.utils import get_output_volume
from tomoscan.factory import Factory
from typing import Iterable
from nabu.stitching.utils import ShiftAlgorithm
from tomoscan.unitsystem.metricsystem import MetricSystem
from math import ceil


KEY_SCORE_METHOD = "score_method"

KEY_IMG_REG_METHOD = "img_reg_method"

KEY_WINDOW_SIZE = "window_size"

KEY_LOW_PASS_FILTER = "low_pass"

KEY_HIGH_PASS_FILTER = "high_pass"

KEY_OVERLAP_SIZE = "overlap_size"

KEY_SIDE = "side"

OUTPUT_SECTION = "output"

INPUTS_SECTION = "inputs"

Z_PRE_PROC_SECTION = "z-preproc"

Z_POST_PROC_SECTION = "z-postproc"

INPUT_DATASETS_FIELD = "input_datasets"

INPUT_PIXEL_SIZE_MM = "pixel_size"

INPUT_VOXEL_SIZE_MM = "voxel_size"

STITCHING_SECTION = "stitching"

STITCHING_STRATEGY_FIELD = "stitching_strategy"

STITCHING_TYPE_FIELD = "type"

DATA_FILE_FIELD = "location"

OVERWRITE_RESULTS_FIELD = "overwrite_results"

DATA_PATH_FIELD = "data_path"

AXIS_0_POS_PX = "axis_0_pos_px"

AXIS_1_POS_PX = "axis_1_pos_px"

AXIS_2_POS_PX = "axis_2_pos_px"

AXIS_0_POS_MM = "axis_0_pos_mm"

AXIS_1_POS_MM = "axis_1_pos_mm"

AXIS_2_POS_MM = "axis_2_pos_mm"

AXIS_0_PARAMS = "axis_0_params"

AXIS_1_PARAMS = "axis_1_params"

AXIS_2_PARAMS = "axis_2_params"

FLIP_LR = "fliplr"

FLIP_UD = "flipud"

NEXUS_VERSION_FIELD = "nexus_version"

OUTPUT_DTYPE = "data_type"

OUTPUT_VOLUME = "output_volume"

STITCHING_SLICES = "slices"

CROSS_CORRELATION_SLICE_FIELD = "slice_index_for_correlation"

RESCALE_FRAMES = "rescale_frames"

RESCALE_PARAMS = "rescale_params"

KEY_RESCALE_MIN_PERCENTILES = "rescale_min_percentile"

KEY_RESCALE_MAX_PERCENTILES = "rescale_max_percentile"

# SLURM

SLURM_SECTION = "slurm"

SLURM_PARTITION = "partition"

SLURM_MEM = "memory"

SLURM_COR_PER_TASKS = "cpu-per-task"

SLURM_NUMBER_OF_TASKS = "n_tasks"

SLURM_N_JOBS = "n_jobs"

SLURM_OTHER_OPTIONS = "other_options"

SLURM_PREPROCESSING_COMMAND = "python_venv"

SLURM_CLEAN_SCRIPTS = "clean_scripts"

# kernel extra options

STITCHING_KERNELS_EXTRA_PARAMS = "stitching_kernels_extra_params"

KEY_THRESHOLD_FREQUENCY = "threshold_frequency"


CROSS_CORRELATION_METHODS_AXIS_0 = {
    "": "",  # for display
    ShiftAlgorithm.NABU_FFT.value: "will call nabu `find_shift_correlate` function - shift search in fourier space",
    ShiftAlgorithm.SKIMAGE.value: "use scikit image `phase_cross_correlation` function in real space",
    ShiftAlgorithm.SHIFT_GRID.value: "will compute a score for each possible shift and pick the shift with the highest score",
    ShiftAlgorithm.NONE.value: "no shift research is done. will only get shift from motor positions",
}

CROSS_CORRELATION_METHODS_AXIS_2 = CROSS_CORRELATION_METHODS_AXIS_0.copy()
CROSS_CORRELATION_METHODS_AXIS_2.update(
    {
        ShiftAlgorithm.CENTERED.value: "a fast and simple auto-CoR method. It only works when the CoR is not far from the middle of the detector. It does not work for half-tomography.",
        ShiftAlgorithm.GLOBAL.value: "a slow but robust auto-CoR.",
        ShiftAlgorithm.GROWING_WINDOW.value: "automatically find the CoR with a sliding-and-growing window. You can tune the option with the parameter 'cor_options'.",
        ShiftAlgorithm.SLIDING_WINDOW.value: "semi-automatically find the CoR with a sliding window. You have to specify on which side the CoR is (left, center, right). Please see the 'cor_options' parameter.",
        ShiftAlgorithm.COMPOSITE_COARSE_TO_FINE.value: "Estimate CoR from composite multi-angle images. Only works for 360 degrees scans.",
        ShiftAlgorithm.SINO_COARSE_TO_FINE.value: "Estimate CoR from sinogram. Only works for 360 degrees scans.",
    }
)

SECTIONS_COMMENTS = {
    STITCHING_SECTION: "section dedicated to stich parameters\n",
    OUTPUT_SECTION: "section dedicated to output parameters\n",
    INPUTS_SECTION: "section dedicated to inputs\n",
    SLURM_SECTION: "section didicated to slurm. If you want to run locally avoid setting 'partition or remove this section'",
}

DEFAULT_SHIFT_ALG_AXIS_0 = "nabu-fft"
DEFAULT_SHIFT_ALG_AXIS_2 = "sliding-window"

_shift_algs_axis_0 = "\n            + ".join(
    [f"{key}: {value}" for key, value in CROSS_CORRELATION_METHODS_AXIS_0.items()]
)
_shift_algs_axis_2 = "\n            + ".join(
    [f"{key}: {value}" for key, value in CROSS_CORRELATION_METHODS_AXIS_2.items()]
)

HELP_SHIFT_PARAMS = f"""options for shifts algorithms as `key1=value1,key2=value2`. For now valid keys are:
    - {KEY_WINDOW_SIZE}: size of the window for the 'shift-grid' algorithm'.
    - {KEY_OVERLAP_SIZE}: size to apply stitching. If not provided will take the largest size possible'.
    - {KEY_SCORE_METHOD}: method to use in order to compute score for the 'shift-grid' algorithm. Values can be 'tv' (total variation), '1/tv', 'std' (standard deviation), '1/std'.
    - {KEY_IMG_REG_METHOD}: algorithm to use to find overlaps between the different sections. Possible values are \n        * for axis 0: {_shift_algs_axis_0}\n        * and for axis 2: {_shift_algs_axis_2}
    - {KEY_LOW_PASS_FILTER}: low pass filter value for filtering frames before shift research
    - {KEY_HIGH_PASS_FILTER}: high pass filter value for filtering frames before shift research"""


def _str_to_dict(my_str: Union[str, dict]):
    """convert a string as key_1=value_2;key_2=value_2 to a dict"""
    if isinstance(my_str, dict):
        return my_str
    res = {}
    for key_value in filter(None, my_str.split(";")):
        key, value = key_value.split("=")
        res[key] = value
    return res


def _dict_to_str(ddict: dict):
    return ";".join([f"{str(key)}={str(value)}" for key, value in ddict.items()])


def str_to_shifts(my_str: Optional[str]) -> Union[str, tuple]:
    if my_str is None:
        return None
    elif isinstance(my_str, str):
        my_str = my_str.replace(" ", "")
        my_str = my_str.lstrip("[").lstrip("(")
        my_str = my_str.rstrip("]").lstrip(")")
        if my_str == "":
            return None
        try:
            shift = ShiftAlgorithm.from_value(my_str)
        except ValueError:
            shifts_as_str = filter(None, my_str.replace(";", ",").split(","))
            return [float(shift) for shift in shifts_as_str]
        else:
            return shift
    elif isinstance(my_str, (tuple, list)):
        return [float(shift) for shift in my_str]
    else:
        raise TypeError("Only str or tuple of str expected expected")


def _valid_stitching_kernels_params(my_dict: Union[dict, str]):
    if isinstance(my_dict, str):
        my_dict = _str_to_dict(my_str=my_dict)

    valid_keys = (KEY_THRESHOLD_FREQUENCY, KEY_SIDE)
    for key in my_dict.keys():
        if not key in valid_keys:
            raise KeyError(f"{key} is a unrecognized key")
    return my_dict


def _valid_shifts_params(my_dict: Union[dict, str]):
    if isinstance(my_dict, str):
        my_dict = _str_to_dict(my_str=my_dict)

    valid_keys = (
        KEY_SCORE_METHOD,
        KEY_WINDOW_SIZE,
        KEY_IMG_REG_METHOD,
        KEY_OVERLAP_SIZE,
        KEY_HIGH_PASS_FILTER,
        KEY_LOW_PASS_FILTER,
        KEY_SIDE,
    )
    for key in my_dict.keys():
        if not key in valid_keys:
            raise KeyError(f"{key} is a unrecognized key")
    return my_dict


def _slices_to_list_or_slice(my_str: Optional[str]) -> Union[str, slice]:
    if my_str is None:
        return None
    if isinstance(my_str, (tuple, list)):
        if len(my_str) == 2:
            return slice(int(my_str[0]), int(my_str[1]))
        elif len(my_str) == 3:
            return slice(int(my_str[0]), int(my_str[1]), int(my_str[2]))
        else:
            raise ValueError("expect at most free values to define a slice")

    assert isinstance(my_str, str), f"wrong type. Get {my_str}, {type(my_str)}"
    my_str = my_str.replace(" ", "")
    if ":" in my_str:
        split_string = my_str.split(":")
        start = int(split_string[0])
        stop = int(split_string[1])
        if len(split_string) == 2:
            step = None
        elif len(split_string) == 3:
            step = int(split_string[2])
        else:
            raise ValueError(f"unable to interpret `slices` parameter: {my_str}")
        return slice(start, stop, step)
    else:
        my_str.replace(",", ";")
        return list(filter(None, my_str.split(";")))


def _scalar_or_tuple_to_bool_or_tuple_of_bool(my_str: Union[bool, tuple, str], default=False):
    if isinstance(my_str, bool):
        return my_str
    elif isinstance(my_str, str):
        my_str = my_str.replace(" ", "")
        my_str = my_str.lstrip("(").lstrip("[")
        my_str = my_str.rstrip(")").lstrip("]")
        my_str = my_str.replace(",", ";")
        values = my_str.split(";")
        values = tuple([convert_to_bool(value)[0] for value in values])
    else:
        values = my_str
    if len(values) == 0:
        return default
    elif len(values) == 1:
        return values[0]
    else:
        return values


@dataclass
class SlurmConfig:
    "configuration for slurm jobs"
    partition: str = ""  # note: must stay empty to make by default we don't use slurm (use by the  configuration file)
    mem: str = "128"
    n_jobs: int = 1
    other_options: str = ""
    preprocessing_command: str = ""
    clean_script: bool = ""
    n_tasks: int = 1
    n_cpu_per_task: int = 4

    def to_dict(self) -> dict:
        "dump configuration to dict"
        return {
            SLURM_PARTITION: self.partition if self.partition is not None else "",
            SLURM_MEM: self.mem,
            SLURM_N_JOBS: self.n_jobs,
            SLURM_OTHER_OPTIONS: self.other_options,
            SLURM_PREPROCESSING_COMMAND: self.preprocessing_command,
            SLURM_CLEAN_SCRIPTS: self.clean_script,
            SLURM_NUMBER_OF_TASKS: self.n_tasks,
            SLURM_COR_PER_TASKS: self.n_cpu_per_task,
        }

    @staticmethod
    def from_dict(config: dict):
        return SlurmConfig(
            partition=config.get(
                SLURM_PARTITION, None
            ),  # warning: never set a default value. Would generate infinite loop from slurm call
            mem=config.get(SLURM_MEM, "32GB"),
            n_jobs=int(config.get(SLURM_N_JOBS, 10)),
            other_options=config.get(SLURM_OTHER_OPTIONS, ""),
            n_tasks=config.get(SLURM_NUMBER_OF_TASKS, 1),
            n_cpu_per_task=config.get(SLURM_COR_PER_TASKS, 4),
            preprocessing_command=config.get(SLURM_PREPROCESSING_COMMAND, ""),
            clean_script=convert_to_bool(config.get(SLURM_CLEAN_SCRIPTS, False))[0],
        )


class StitchingType(_Enum):
    Z_PREPROC = "z-preproc"
    Z_POSTPROC = "z-postproc"


def _cast_shift_to_str(shifts: Union[tuple, str, None]) -> str:
    if shifts is None:
        return ""
    elif isinstance(shifts, ShiftAlgorithm):
        return shifts.value
    elif isinstance(shifts, str):
        return shifts
    elif isinstance(shifts, (tuple, list)):
        return ";".join([str(value) for value in shifts])


@dataclass
class StitchingConfiguration:
    """
    bass class to define stitching configuration
    """

    axis_0_pos_px: Union[tuple, str, None]
    "position along axis 0 in absolute. unit: px"
    axis_1_pos_px: Union[tuple, str, None]
    "position along axis 1 in absolute. unit: px"
    axis_2_pos_px: Union[tuple, str, None]
    "position along axis 2 in absolute. unit: px"

    axis_0_pos_mm: Union[tuple, str, None] = None
    "position along axis 0 in absolute. unit: mm"
    axis_1_pos_mm: Union[tuple, str, None] = None
    "position along axis 0 in absolute. unit: mm"
    axis_2_pos_mm: Union[tuple, str, None] = None
    "position along axis 0 in absolute. unit: mm"

    axis_0_params: dict = None
    axis_1_params: dict = None
    axis_2_params: dict = None
    slurm_config: SlurmConfig = None
    flip_lr: Union[tuple, bool] = False
    "flip frame left-right. For scan this will happen after possible flip of NXtomo metadata x_flipped field (also know as lr_flipped)"
    flip_ud: Union[tuple, bool] = False
    "flip frame up-down. For scan this will happen after possible flip of NXtomo metadata y_flipped field (also know as ud_flipped)"

    overwrite_results: bool = False
    stitching_strategy: OverlapStitchingStrategy = OverlapStitchingStrategy.COSINUS_WEIGHTS
    stitching_kernels_extra_params: dict = None

    slice_for_cross_correlation: Union[str, int] = "middle"

    # opts for rescaling frame during stitching
    rescale_frames: bool = False
    rescale_params: dict = None

    @property
    def stitching_type(self):
        raise NotImplementedError("Base class")

    @staticmethod
    def get_description_dict() -> dict:
        def get_pos_info(axis, unit, alternative):
            return f"position over {axis} in {unit}. If provided {alternative} must be set to blank. If none provided then will try to get information from existing metadata"

        def get_default_shift_params(window_size=None, shift_alg=None) -> str:
            return ";".join(
                [
                    f"{KEY_WINDOW_SIZE}={window_size or ''}",
                    f"{KEY_IMG_REG_METHOD}={shift_alg or ''}",
                ]
            )

        return {
            STITCHING_SECTION: {
                STITCHING_TYPE_FIELD: {
                    "default": StitchingType.Z_PREPROC.value,
                    "help": f"stitching to be applied. Must be in {StitchingType.values()}",
                    "type": "required",
                },
                STITCHING_STRATEGY_FIELD: {
                    "default": "cosinus weights",
                    "help": f"Policy to apply to compute the overlap area. Must be in {OverlapStitchingStrategy.values()}.",
                    "type": "required",
                },
                CROSS_CORRELATION_SLICE_FIELD: {
                    "default": "middle",
                    "help": f"slice to use for image registration",
                    "type": "optional",
                },
                AXIS_0_POS_PX: {
                    "default": "",
                    "help": get_pos_info(axis=0, unit="pixel", alternative=AXIS_0_POS_MM),
                    "type": "optional",
                },
                AXIS_0_POS_MM: {
                    "default": "",
                    "help": get_pos_info(axis=1, unit="millimeter", alternative=AXIS_0_POS_PX),
                    "type": "optional",
                },
                AXIS_0_PARAMS: {
                    "default": get_default_shift_params(window_size=50, shift_alg=DEFAULT_SHIFT_ALG_AXIS_0),
                    "help": HELP_SHIFT_PARAMS,
                    "type": "optional",
                },
                AXIS_1_POS_PX: {
                    "default": "",
                    "help": get_pos_info(axis=1, unit="pixel", alternative=AXIS_1_POS_MM),
                    "type": "optional",
                },
                AXIS_1_POS_MM: {
                    "default": "",
                    "help": get_pos_info(axis=1, unit="millimeter", alternative=AXIS_1_POS_PX),
                    "type": "optional",
                },
                AXIS_1_PARAMS: {
                    "default": get_default_shift_params(),
                    "help": f"same as {AXIS_0_PARAMS} but for axis 1",
                    "type": "optional",
                },
                AXIS_2_POS_PX: {
                    "default": "",
                    "help": get_pos_info(axis=2, unit="pixel", alternative=AXIS_2_POS_MM),
                    "type": "optional",
                },
                AXIS_2_POS_MM: {
                    "default": "",
                    "help": get_pos_info(axis=2, unit="millimeter", alternative=AXIS_1_POS_PX),
                    "type": "optional",
                },
                AXIS_2_PARAMS: {
                    "default": get_default_shift_params(window_size=200, shift_alg=DEFAULT_SHIFT_ALG_AXIS_2),
                    "help": f"same as {AXIS_0_PARAMS} but for axis 2",
                    "type": "optional",
                },
                FLIP_LR: {
                    "default": False,
                    "help": "sometime scan or volume can have a left-right flip in frame (projection/slice) space. For recent NXtomo it should be handled automatically. But for volume you might need to request some flip.",
                    "type": "optional",
                },
                FLIP_UD: {
                    "default": False,
                    "help": "sometime scan or volume can have a up_down flip in frame (projection/slice) space. For recent NXtomo it should be handled automatically. But for volume you might need to request some flip.",
                    "type": "optional",
                },
                RESCALE_FRAMES: {
                    "default": False,
                    "help": "rescale each frame before applying stithcing",
                    "type": "advanced",
                },
                RESCALE_PARAMS: {
                    "default": "",
                    "help": f"parameters for rescaling frames as 'key1=value1;key_2=value2'. Valid Keys are {KEY_RESCALE_MIN_PERCENTILES} and {KEY_RESCALE_MAX_PERCENTILES}.",
                    "type": "advanced",
                },
                STITCHING_KERNELS_EXTRA_PARAMS: {
                    "default": "",
                    "help": f"advanced parameters for some stitching kernels. must be provided as 'key1=value1;key_2=value2'. Valid keys for now are: {KEY_THRESHOLD_FREQUENCY}: threshold to be used by the {OverlapStitchingStrategy.IMAGE_MINIMUM_DIVERGENCE.value} to split images low and high frequencies in Fourier space.",
                    "type": "advanced",
                },
            },
            OUTPUT_SECTION: {
                OVERWRITE_RESULTS_FIELD: {
                    "default": "1",
                    "help": "What to do in the case where the output file exists.\nBy default, the output data is never overwritten and the process is interrupted if the file already exists.\nSet this option to 1 if you want to overwrite the output files.",
                    "validator": boolean_validator,
                    "type": "required",
                },
            },
            INPUTS_SECTION: {
                INPUT_DATASETS_FIELD: {
                    "default": "",
                    "help": f"Dataset to stitch together. Must be volume for {StitchingType.Z_PREPROC.value} or NXtomo for {StitchingType.Z_POSTPROC.value}",
                    "type": "required",
                },
                STITCHING_SLICES: {
                    "default": "",
                    "help": f"slices to be stitched. Must be given along axis 0 for pre-processing (z) and along axis 1 for post-processing (y)",
                    "type": "advanced",
                },
            },
            SLURM_SECTION: {
                SLURM_PARTITION: {
                    "default": "",
                    "help": "slurm partition to be used. If empty will run locally",
                    "type": "optional",
                },
                SLURM_MEM: {
                    "default": "32GB",
                    "help": "memory to allocate for each job",
                    "type": "optional",
                },
                SLURM_N_JOBS: {
                    "default": 10,
                    "help": "number of job to launch (split computation on N parallel jobs). Once all are finished we will concatenate the result.",
                    "type": "optional",
                },
                SLURM_COR_PER_TASKS: {
                    "default": 4,
                    "help": "number of cor per task launched",
                    "type": "optional",
                },
                SLURM_NUMBER_OF_TASKS: {
                    "default": 1,
                    "help": "(for parallel execution when possible). Split each job into this number of tasks",
                    "type": "optional",
                },
                SLURM_OTHER_OPTIONS: {
                    "default": "",
                    "help": "you can provide axtra options to slurm from this string",
                    "type": "optional",
                },
                SLURM_PREPROCESSING_COMMAND: {
                    "default": "'/scisoft/tomotools_env/activate.sh stable'",
                    "help": "python virtual environment to use",
                    "type": "optional",
                },
            },
        }

    def to_dict(self):
        """dump configuration to a dict. Must be serializable because might be dump to HDF5 file"""
        return {
            SLURM_SECTION: self.slurm_config.to_dict() if self.slurm_config is not None else SlurmConfig().to_dict(),
            STITCHING_SECTION: {
                STITCHING_TYPE_FIELD: self.stitching_type.value,
                CROSS_CORRELATION_SLICE_FIELD: str(self.slice_for_cross_correlation),
                AXIS_0_POS_PX: _cast_shift_to_str(self.axis_0_pos_px),
                AXIS_0_POS_MM: _cast_shift_to_str(self.axis_0_pos_mm),
                AXIS_0_PARAMS: _dict_to_str(self.axis_0_params or {}),
                AXIS_1_POS_PX: _cast_shift_to_str(self.axis_1_pos_px),
                AXIS_1_POS_MM: _cast_shift_to_str(self.axis_1_pos_mm),
                AXIS_1_PARAMS: _dict_to_str(self.axis_1_params or {}),
                AXIS_2_POS_PX: _cast_shift_to_str(self.axis_2_pos_px),
                AXIS_2_POS_MM: _cast_shift_to_str(self.axis_2_pos_mm),
                AXIS_2_PARAMS: _dict_to_str(self.axis_2_params or {}),
                STITCHING_STRATEGY_FIELD: OverlapStitchingStrategy.from_value(self.stitching_strategy).value,
                FLIP_UD: self.flip_ud,
                FLIP_LR: self.flip_lr,
                RESCALE_FRAMES: self.rescale_frames,
                RESCALE_PARAMS: _dict_to_str(self.rescale_params or {}),
                STITCHING_KERNELS_EXTRA_PARAMS: _dict_to_str(self.stitching_kernels_extra_params or {}),
            },
            OUTPUT_SECTION: {
                OVERWRITE_RESULTS_FIELD: int(
                    self.overwrite_results,
                ),
            },
        }


@dataclass
class ZStitchingConfiguration(StitchingConfiguration):
    """
    base class to define z-stitching parameters
    """

    slices: Union[
        slice, tuple, None
    ] = None  # slices to reconstruct. Over axis 0 for pre-processing, over axis 1 for post-processing. If None will reconstruct all

    def settle_inputs(self) -> None:
        self.settle_slices()

    def settle_slices(self) -> tuple:
        raise ValueError("Base class")

    def get_output_object(self):
        raise ValueError("Base class")

    def to_dict(self):
        if isinstance(self.slices, slice):
            slices = f"{self.slices.start}:{self.slices.stop}:{self.slices.step}"
        elif self.slices in ("", None):
            slices = ""
        else:
            slices = ";".join(str(s) for s in self.slices)
        return concatenate_dict(
            super().to_dict(),
            {
                INPUTS_SECTION: {
                    STITCHING_SLICES: slices,
                }
            },
        )


@dataclass
class PreProcessedZStitchingConfiguration(ZStitchingConfiguration):
    """
    base class to define z-stitching parameters
    """

    input_scans: tuple = ()  # tuple of ScanBase
    output_file_path: str = ""
    output_data_path: str = ""
    output_nexus_version: Optional[float] = None
    pixel_size: Optional[float] = None

    @property
    def stitching_type(self) -> StitchingType:
        return StitchingType.Z_PREPROC

    def get_output_object(self):
        return HDF5TomoScan(
            scan=self.output_file_path,
            entry=self.output_data_path,
        )

    def settle_inputs(self) -> None:
        super().settle_inputs()
        self.settle_input_scans()

    def settle_input_scans(self):
        self.input_scans = [
            Factory.create_tomo_object_from_identifier(identifier)
            if isinstance(identifier, (str, ScanIdentifier))
            else identifier
            for identifier in self.input_scans
        ]

    def slice_idx_from_str_to_int(self, index):
        if isinstance(index, str):
            index = index.lower()
            if index == "first":
                return 0
            elif index == "last":
                return len(self.input_scans[0].projections) - 1
            elif index == "middle":
                return max(len(self.input_scans[0].projections) // 2 - 1, 0)
        return int(index)

    def settle_slices(self) -> tuple:
        """
        interpret the slices to be stitched if needed

        Nore: if slices is an instance of slice will redefine start and stop to avoid having negative indexes

        :return: (slices:[slice,Iterable], n_proj:int)
        :rtype: tuple
        """
        slices = self.slices
        if isinstance(slices, Sized) and len(slices) == 0:
            # in this case will stitch them all
            slices = None
        if len(self.input_scans) == 0:
            raise ValueError("No input scan provided")
        if slices is None:
            slices = slice(0, len(self.input_scans[0].projections), 1)
            n_proj = slices.stop
        elif isinstance(slices, slice):
            # force slices indices to be positive
            start = slices.start
            if start < 0:
                start += len(self.input_scans[0].projections) + 1
            stop = slices.stop
            if stop < 0:
                stop += len(self.input_scans[0].projections) + 1
            step = slices.step
            if step is None:
                step = 1
            n_proj = ceil((stop - start) / step)
            # update slices for iteration simplify things
            slices = slice(start, stop, step)
        elif isinstance(slices, (tuple, list)):
            n_proj = len(slices)
            slices = [self.slice_idx_from_str_to_int(s) for s in slices]
        else:
            raise TypeError(f"slices is expected to be a tuple or a lice. Not {type(slices)}")
        self.slices = slices
        return slices, n_proj

    def to_dict(self):
        if self.pixel_size is None:
            pixel_size_mm = ""
        else:
            pixel_size_mm = self.pixel_size * MetricSystem.MILLIMETER.value
        return concatenate_dict(
            super().to_dict(),
            {
                Z_PRE_PROC_SECTION: {
                    DATA_FILE_FIELD: self.output_file_path,
                    DATA_PATH_FIELD: self.output_data_path,
                    NEXUS_VERSION_FIELD: self.output_nexus_version,
                },
                INPUTS_SECTION: {
                    INPUT_DATASETS_FIELD: ";".join(
                        [str(scan.get_identifier()) for scan in self.input_scans],
                    ),
                    INPUT_PIXEL_SIZE_MM: pixel_size_mm,
                },
            },
        )

    @staticmethod
    def get_description_dict() -> dict:
        return concatenate_dict(
            ZStitchingConfiguration.get_description_dict(),
            {
                Z_PRE_PROC_SECTION: {
                    DATA_FILE_FIELD: {
                        "default": "",
                        "help": "output nxtomo file path",
                        "type": "required",
                    },
                    DATA_PATH_FIELD: {
                        "default": "",
                        "help": "output nxtomo data path",
                        "type": "required",
                    },
                    NEXUS_VERSION_FIELD: {
                        "default": "",
                        "help": "nexus version. If not provided will pick the latest one know",
                        "type": "required",
                    },
                },
            },
        )

    @staticmethod
    def from_dict(config: dict):
        if not isinstance(config, dict):
            raise TypeError(f"config is expected to be a dict and not {type(config)}")
        inputs_scans_str = config.get(INPUTS_SECTION, {}).get(INPUT_DATASETS_FIELD, None)
        if inputs_scans_str in (None, ""):
            input_scans = []
        else:
            input_scans = identifiers_as_str_to_instances(inputs_scans_str)

        output_file_path = config.get(Z_PRE_PROC_SECTION, {}).get(DATA_FILE_FIELD, None)

        nexus_version = config.get(Z_PRE_PROC_SECTION, {}).get(NEXUS_VERSION_FIELD, None)
        if nexus_version in (None, ""):
            nexus_version = nxtomo.LATEST_VERSION
        else:
            nexus_version = float(nexus_version)
        pixel_size = config.get(INPUT_PIXEL_SIZE_MM, "").replace(" ", "")
        if pixel_size == "":
            pixel_size = None
        else:
            pixel_size = float(pixel_size) / MetricSystem.MM

        return PreProcessedZStitchingConfiguration(
            stitching_strategy=OverlapStitchingStrategy.from_value(
                config[STITCHING_SECTION].get(
                    STITCHING_STRATEGY_FIELD,
                    OverlapStitchingStrategy.COSINUS_WEIGHTS,
                ),
            ),
            axis_0_pos_px=str_to_shifts(config[STITCHING_SECTION].get(AXIS_0_POS_PX, None)),
            axis_0_pos_mm=str_to_shifts(config[STITCHING_SECTION].get(AXIS_0_POS_MM, None)),
            axis_0_params=_valid_shifts_params(_str_to_dict(config[STITCHING_SECTION].get(AXIS_0_PARAMS, {}))),
            axis_1_pos_px=str_to_shifts(config[STITCHING_SECTION].get(AXIS_1_POS_PX, None)),
            axis_1_pos_mm=str_to_shifts(config[STITCHING_SECTION].get(AXIS_1_POS_MM, None)),
            axis_1_params=_valid_shifts_params(
                _str_to_dict(
                    config[STITCHING_SECTION].get(AXIS_1_PARAMS, {}),
                )
            ),
            axis_2_pos_px=str_to_shifts(config[STITCHING_SECTION].get(AXIS_2_POS_PX, None)),
            axis_2_pos_mm=str_to_shifts(config[STITCHING_SECTION].get(AXIS_2_POS_MM, None)),
            axis_2_params=_valid_shifts_params(
                _str_to_dict(
                    config[STITCHING_SECTION].get(AXIS_2_PARAMS, {}),
                )
            ),
            input_scans=input_scans,
            output_file_path=output_file_path,
            output_data_path=config.get(Z_PRE_PROC_SECTION, {}).get(DATA_PATH_FIELD, "entry_from_stitchig"),
            overwrite_results=config[STITCHING_SECTION].get(OVERWRITE_RESULTS_FIELD, True),
            output_nexus_version=nexus_version,
            slices=_slices_to_list_or_slice(config[INPUTS_SECTION].get(STITCHING_SLICES, None)),
            slurm_config=SlurmConfig.from_dict(config.get(SLURM_SECTION, {})),
            slice_for_cross_correlation=config[STITCHING_SECTION].get(CROSS_CORRELATION_SLICE_FIELD, "middle"),
            pixel_size=pixel_size,
            flip_ud=_scalar_or_tuple_to_bool_or_tuple_of_bool(config[STITCHING_SECTION].get(FLIP_UD, False)),
            flip_lr=_scalar_or_tuple_to_bool_or_tuple_of_bool(config[STITCHING_SECTION].get(FLIP_LR, False)),
            rescale_frames=convert_to_bool(config[STITCHING_SECTION].get(RESCALE_FRAMES, 0))[0],
            rescale_params=_str_to_dict(config[STITCHING_SECTION].get(RESCALE_PARAMS, {})),
            stitching_kernels_extra_params=_valid_stitching_kernels_params(
                _str_to_dict(
                    config[STITCHING_SECTION].get(STITCHING_KERNELS_EXTRA_PARAMS, {}),
                )
            ),
        )


@dataclass
class PostProcessedZStitchingConfiguration(ZStitchingConfiguration):
    """
    base class to define z-stitching parameters
    """

    input_volumes: tuple = ()  # tuple of VolumeBase
    output_volume: Optional[VolumeIdentifier] = None
    voxel_size: Optional[float] = None

    @property
    def stitching_type(self) -> StitchingType:
        return StitchingType.Z_POSTPROC

    def get_output_object(self):
        return self.output_volume

    def settle_inputs(self) -> None:
        super().settle_inputs()
        self.settle_input_volumes()

    def settle_input_volumes(self):
        self.input_volumes = [
            Factory.create_tomo_object_from_identifier(identifier)
            if isinstance(identifier, (str, VolumeIdentifier))
            else identifier
            for identifier in self.input_volumes
        ]

    def slice_idx_from_str_to_int(self, index):
        if isinstance(index, str):
            index = index.lower()
            if index == "first":
                return 0
            elif index == "last":
                return self.input_volumes[0].get_volume_shape()[1] - 1
            elif index == "middle":
                return max(self.input_volumes[0].get_volume_shape()[1] // 2 - 1, 0)
        return int(index)

    def settle_slices(self) -> tuple:
        """
        interpret the slices to be stitched if needed

        Nore: if slices is an instance of slice will redefine start and stop to avoid having negative indexes

        :return: (slices:[slice,Iterable], n_proj:int)
        :rtype: tuple
        """
        slices = self.slices
        if isinstance(slices, Sized) and len(slices) == 0:
            # in this case will stitch them all
            slices = None
        if len(self.input_volumes) == 0:
            raise ValueError("No input volume provided. Cannot settle slices")
        if slices is None:
            slices = slice(0, self.input_volumes[0].get_volume_shape()[1], 1)
            n_slices = slices.stop
        if isinstance(slices, slice):
            # force slices indices to be positive
            start = slices.start
            if start < 0:
                start += self.input_volumes[0].get_volume_shape()[1] + 1
            stop = slices.stop
            if stop < 0:
                stop += self.input_volumes[0].get_volume_shape()[1] + 1
            step = slices.step
            if step is None:
                step = 1
            n_slices = ceil((stop - start) / step)
            # update slices for iteration simplify things
            slices = slice(start, stop, step)
        elif isinstance(slices, Iterable):
            n_slices = len(slices)
            slices = [self.slice_idx_from_str_to_int(s) for s in slices]
        else:
            raise TypeError(f"slices is expected to be a tuple or a slice. Not {type(slices)}")
        self.slices = slices
        return slices, n_slices

    @staticmethod
    def from_dict(config: dict):
        if not isinstance(config, dict):
            raise TypeError(f"config is expected to be a dict and not {type(config)}")
        inputs_volumes_str = config.get(INPUTS_SECTION, {}).get(INPUT_DATASETS_FIELD, None)
        if inputs_volumes_str in (None, ""):
            input_volumes = []
        else:
            input_volumes = identifiers_as_str_to_instances(inputs_volumes_str)
        overwrite_results = config[STITCHING_SECTION].get(OVERWRITE_RESULTS_FIELD, True) in ("1", True, "True", 1)
        output_volume = config.get(Z_POST_PROC_SECTION, {}).get(OUTPUT_VOLUME, None)
        if output_volume is not None:
            output_volume = Factory.create_tomo_object_from_identifier(output_volume)
            output_volume.overwrite = overwrite_results
        voxel_size = config.get(INPUTS_SECTION, {}).get(INPUT_VOXEL_SIZE_MM, "")
        voxel_size = voxel_size.replace(" ", "")
        if voxel_size == "":
            voxel_size = None
        else:
            voxel_size = float(voxel_size) * MetricSystem.MM

        # on the next section the one with a default value qre the optionnal one
        return PostProcessedZStitchingConfiguration(
            stitching_strategy=OverlapStitchingStrategy.from_value(
                config[STITCHING_SECTION].get(
                    STITCHING_STRATEGY_FIELD,
                    OverlapStitchingStrategy.COSINUS_WEIGHTS,
                ),
            ),
            axis_0_pos_px=str_to_shifts(config[STITCHING_SECTION].get(AXIS_0_POS_PX, None)),
            axis_0_pos_mm=str_to_shifts(config[STITCHING_SECTION].get(AXIS_0_POS_MM, None)),
            axis_0_params=_valid_shifts_params(config[STITCHING_SECTION].get(AXIS_0_PARAMS, {})),
            axis_1_pos_px=str_to_shifts(config[STITCHING_SECTION].get(AXIS_1_POS_PX, None)),
            axis_1_pos_mm=str_to_shifts(config[STITCHING_SECTION].get(AXIS_1_POS_MM, None)),
            axis_1_params=_valid_shifts_params(config[STITCHING_SECTION].get(AXIS_1_PARAMS, {})),
            axis_2_pos_px=str_to_shifts(config[STITCHING_SECTION].get(AXIS_2_POS_PX, None)),
            axis_2_pos_mm=str_to_shifts(config[STITCHING_SECTION].get(AXIS_2_POS_MM, None)),
            axis_2_params=_valid_shifts_params(config[STITCHING_SECTION].get(AXIS_2_PARAMS, {})),
            input_volumes=input_volumes,
            output_volume=output_volume,
            overwrite_results=overwrite_results,
            slices=_slices_to_list_or_slice(config[INPUTS_SECTION].get(STITCHING_SLICES, None)),
            slurm_config=SlurmConfig.from_dict(config.get(SLURM_SECTION, {})),
            voxel_size=voxel_size,
            slice_for_cross_correlation=config[STITCHING_SECTION].get(CROSS_CORRELATION_SLICE_FIELD, "middle"),
            flip_ud=_scalar_or_tuple_to_bool_or_tuple_of_bool(config[STITCHING_SECTION].get(FLIP_UD, False)),
            flip_lr=_scalar_or_tuple_to_bool_or_tuple_of_bool(config[STITCHING_SECTION].get(FLIP_LR, False)),
            rescale_frames=convert_to_bool(config[STITCHING_SECTION].get(RESCALE_FRAMES, 0))[0],
            rescale_params=_str_to_dict(config[STITCHING_SECTION].get(RESCALE_PARAMS, {})),
            stitching_kernels_extra_params=_valid_stitching_kernels_params(
                _str_to_dict(
                    config[STITCHING_SECTION].get(STITCHING_KERNELS_EXTRA_PARAMS, {}),
                )
            ),
        )

    def to_dict(self):
        if self.voxel_size is None:
            voxel_size_mm = ""
        else:
            voxel_size_mm = numpy.array(self.voxel_size) / MetricSystem.MM

        return concatenate_dict(
            super().to_dict(),
            {
                INPUTS_SECTION: {
                    INPUT_DATASETS_FIELD: [volume.get_identifier().to_str() for volume in self.input_volumes],
                    INPUT_VOXEL_SIZE_MM: voxel_size_mm,
                },
                Z_POST_PROC_SECTION: {
                    OUTPUT_VOLUME: self.output_volume.get_identifier().to_str()
                    if self.output_volume is not None
                    else "",
                },
            },
        )

    @staticmethod
    def get_description_dict() -> dict:
        return concatenate_dict(
            ZStitchingConfiguration.get_description_dict(),
            {
                Z_POST_PROC_SECTION: {
                    OUTPUT_VOLUME: {
                        "default": "",
                        "help": "identifier of the output volume. Like hdf5:volume:[file_path]?path=[data_path] for an HDF5 volume",
                        "type": "required",
                    },
                },
            },
        )


def identifiers_as_str_to_instances(list_identifiers_as_str: str) -> tuple:
    # convert str to a list of str that should represent identifiers
    if isinstance(list_identifiers_as_str, str):
        list_identifiers_as_str = list_identifiers_as_str.lstrip("[").lstrip("(")
        list_identifiers_as_str = list_identifiers_as_str.rstrip("]").rstrip(")")
        identifiers_as_str = convert_str_to_tuple(list_identifiers_as_str.replace(";", ","))
    else:
        identifiers_as_str = list_identifiers_as_str
    if identifiers_as_str is None:
        return tuple()
    # convert identifiers as string to IdentifierType instances
    return tuple(
        [Factory.create_tomo_object_from_identifier(identifier_as_str) for identifier_as_str in identifiers_as_str]
    )


def dict_to_config_obj(config: dict):
    if not isinstance(config, dict):
        raise TypeError
    stitching_type = config.get(STITCHING_SECTION, {}).get(STITCHING_TYPE_FIELD, None)
    if stitching_type is None:
        raise ValueError("Unagle to find stitching type from config dict")
    else:
        stitching_type = StitchingType.from_value(stitching_type)
        if stitching_type is StitchingType.Z_POSTPROC:
            return PostProcessedZStitchingConfiguration.from_dict(config)
        elif stitching_type is StitchingType.Z_PREPROC:
            return PreProcessedZStitchingConfiguration.from_dict(config)
        else:
            raise NotImplementedError(f"stitching type {stitching_type.value} not handled yet")


def get_default_stitching_config(stitching_type: Optional[Union[StitchingType, str]]) -> tuple:
    """
    Return a default configuration for doing stitching.

    :param stitching_type: if None then return a configuration were use can provide inputs for any
                           of the stitching.
                           Else return config dict dedicated to a particular stitching
    :return: (config, section comments)
    """
    if stitching_type is None:
        return concatenate_dict(z_postproc_stitching_config, z_preproc_stitching_config)

    stitching_type = StitchingType.from_value(stitching_type)
    if stitching_type is StitchingType.Z_POSTPROC:
        return z_postproc_stitching_config
    elif stitching_type is StitchingType.Z_PREPROC:
        return z_preproc_stitching_config
    else:
        raise NotImplementedError


z_preproc_stitching_config = PreProcessedZStitchingConfiguration.get_description_dict()

z_postproc_stitching_config = PostProcessedZStitchingConfiguration.get_description_dict()
