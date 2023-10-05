from os import remove
import numpy as np
from .. import version
from .reconstruct import get_reconstructor
from .cli_configs import MultiCorConfig
from .utils import parse_params_values
from ..utils import view_as_images_stack


def get_user_cors(cors):
    """
    From a user-provided str describing the centers of rotation, build a list.
    """
    cors = cors.strip("[()]")
    cors = cors.split(",")
    cors = [c.strip() for c in cors]
    cors_list = []
    for c in cors:
        if ":" in c:
            if c.count(":") != 2:
                raise ValueError("Malformed range format for '%s': expected format start:stop:step" % c)
            start, stop, step = c.split(":")
            c_list = np.arange(float(start), float(stop), float(step)).tolist()
        else:
            c_list = [float(c)]
        cors_list.extend(c_list)
    return cors_list


def main():
    args = parse_params_values(
        MultiCorConfig,
        parser_description=f"Perform a tomographic reconstruction of a single slice using multiple centers of rotation",
        program_version="nabu " + version,
    )

    reconstructor = get_reconstructor(args)

    if reconstructor.delta_z > 1:
        raise ValueError("Only slice reconstruction can be used (have delta_z = %d)" % reconstructor.delta_z)

    reconstructor.reconstruct()  # warm-up, spawn pipeline

    pipeline = reconstructor.pipeline
    file_prefix = pipeline.processing_options["save"]["file_prefix"]
    #####
    # Remove the first reconstructed file (not used here)
    last_file = list(pipeline.writer.writer.browse_data_files())[-1]
    try:
        remove(last_file)
    except:
        pass
    ######

    cors = get_user_cors(args["cor"])

    all_recs = []

    for cor in cors:
        # Re-configure with new CoR
        pipeline.processing_options["reconstruction"]["rotation_axis_position"] = cor
        pipeline.processing_options["save"]["file_prefix"] = file_prefix + "_%.03f" % cor
        pipeline.reconstruction.reset_rot_center(cor)
        pipeline._init_writer(create_subfolder=False)

        # Get sinogram into contiguous array
        # TODO Can't do memcpy2D ?! It used to work in cuda 11.
        # For now: transfer to host... not optimal
        sino = pipeline._d_radios[:, pipeline._d_radios.shape[1] // 2, :].get()  # pylint: disable=E1136

        # Run reconstruction
        rec = pipeline.reconstruction.fbp(sino)
        # if return_all_recs:
        # all_recs.append(rec)
        rec_3D = view_as_images_stack(rec)  # writer wants 3D data

        # Write
        pipeline.writer.write_data(rec_3D)
        reconstructor.logger.info("Wrote %s" % pipeline.writer.fname)

    return 0


if __name__ == "__main__":
    main()
