import logging
import os
import sys
import numpy as np
import re

from nabu.resources.dataset_analyzer import HDF5DatasetAnalyzer
from nabu.pipeline.estimators import CompositeCOREstimator
from nabu.resources.nxflatfield import update_dataset_info_flats_darks
from .. import version
from .cli_configs import CompositeCorConfig
from .utils import parse_params_values
from ..utils import DictToObj
import json


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def main(user_args=None):
    "Application to extract with the composite cor finder the center of rotation for a scan or a series of scans"

    if user_args is None:
        user_args = sys.argv[1:]

    args_dict = parse_params_values(
        CompositeCorConfig,
        parser_description=main.__doc__,
        program_version="nabu " + version,
        user_args=user_args,
    )
    composite_cor_entry_point(args_dict)
    # here we have been called by the cli. The return value 0 means OK
    return 0


def composite_cor_entry_point(args_dict):
    args = DictToObj(args_dict)

    if len(os.path.dirname(args.filename_template)) == 0:
        # To make sure that other utility routines can succesfully deal with path within the current directory
        args.filename_template = os.path.join(".", args.filename_template)

    args.filename_template = os.path.abspath(args.filename_template)
    if args.first_stage is not None:
        if args.num_of_stages is None:
            args.num_of_stages = 1
        # if the first_stage parameter has been given then
        # we are using numbers to form the names of the files.
        # The filename must containe a XX..X substring which will be replaced
        pattern = re.compile("[X]+")
        ps = pattern.findall(args.filename_template)
        if len(ps) == 0:
            message = f""" You have specified the "first_stage" parameter, with an integer.
            Therefore the "filename_template" parameter is expected to containe a XX..X subsection
            but none was found in the passed parameter which is {args.filename_template}
            """
            raise ValueError(message)
        ls = list(map(len, ps))
        idx = np.argmax(ls)

        args.filename_template = args.filename_template.replace(ps[idx], "{i_stage:" + "0" + str(ls[idx]) + "d}")

    if args.num_of_stages is None:
        # this way it works also in the simple case where
        # only the filename is provided together with the cor options
        num_of_stages = 1
        first_stage = 0
    else:
        num_of_stages = args.num_of_stages
        first_stage = args.first_stage
    cor_list = []
    for iz in range(first_stage, first_stage + num_of_stages):
        if args.num_of_stages is not None:
            nexus_name = args.filename_template.format(i_stage=iz)
        else:
            nexus_name = args.filename_template

        dataset_info = HDF5DatasetAnalyzer(nexus_name, extra_options={"h5_entry": args.entry_name})
        update_dataset_info_flats_darks(dataset_info, flatfield_mode=1)
        cor_finder = CompositeCOREstimator(
            dataset_info,
            oversampling=args.oversampling,
            theta_interval=args.theta_interval,
            n_subsampling_y=args.n_subsampling_y,
            take_log=True,
            spike_threshold=0.04,
            cor_options=args.cor_options,
            norm_order=1,
        )

        cor_position = cor_finder.find_cor()

        cor_list.append(cor_position)

    cor_list = np.array(cor_list).T

    if args.output_file is not None:
        output_name = args.output_file
    else:
        output_name = os.path.splitext(args.filename_template)[0] + "_cors.txt"

    if output_name.endswith(".json"):
        with open(output_name, "w") as fp:
            json.dump(
                dict(rotation_axis_position=cor_list[0], rotation_axis_position_list=cor_list),
                fp,
                indent=4,
                cls=NumpyArrayEncoder,
            )
    else:
        np.savetxt(
            output_name,
            cor_list,
        )
