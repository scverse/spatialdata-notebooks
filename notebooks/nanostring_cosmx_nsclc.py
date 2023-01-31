##

import os
import time

import dask_image.ndinterp
import matplotlib.pyplot as plt
import numpy as np
import spatialdata as sd
from napari_spatialdata import Interactive
from spatialdata._core.core_utils import cyx_cs, get_default_coordinate_system, xy_cs

os.environ["NAPARI_ASYNC"] = "1"
os.environ["NAPARI_OCTREE"] = "1"

zarr_path = "data/spatialdata-sandbox/nanostring_cosmx/data.zarr"
sdata = sd.read_zarr(zarr_path)
SAVE_DATA = False
##
if not SAVE_DATA:
    ##
    # Interactive(sdata)
    points_reference = sdata.points["reference_1"].to_pandas().values
    points_moving = sdata.points["moving_1"].to_pandas().values
    from skimage.transform import SimilarityTransform

    model = SimilarityTransform(dimensionality=2)
    model.estimate(points_moving, points_reference)
    transform_matrix = model.params
    print(transform_matrix)
    xy_cs = get_default_coordinate_system(("x", "y"))  # noqa: F811
    cyx_cs = get_default_coordinate_system(("c", "y", "x"))  # noqa: F811
    affine = sd.Affine(transform_matrix, input_coordinate_system=xy_cs, output_coordinate_system=xy_cs)
    old_moving = sd.get_transform(sdata.images["scaled1"]).to_affine()
    old_reference = sd.get_transform(sdata.images["1"]).to_affine()
    ##
    # verbose, this will be simplified in a refactoring of the spatialdata API
    cyx_to_xy = sd.Affine(
        np.array([[0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]),
        input_coordinate_system=cyx_cs,
        output_coordinate_system=xy_cs,
    )
    xy_to_cyx = sd.Affine(
        np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0], [0, 0, 1]]),
        input_coordinate_system=xy_cs,
        output_coordinate_system=cyx_cs,
    )
    composed = sd.Sequence(
        [old_moving, cyx_to_xy, affine, xy_to_cyx, old_reference.inverse()],
        input_coordinate_system=cyx_cs,
        output_coordinate_system=cyx_cs,
    )
    sd.set_transform(sdata.images["scaled1"], composed)
    Interactive(sdata)

    ##
else:
    ##
    im = sdata.images["1"]
    k = 0.5
    scale = sd.Scale([k, k], input_coordinate_system=xy_cs, output_coordinate_system=xy_cs)
    theta = np.pi / 6
    rotation = sd.Affine(
        np.array(
            [
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1],
            ]
        ),
        input_coordinate_system=xy_cs,
        output_coordinate_system=xy_cs,
    )
    sequence = sd.Sequence([rotation, scale], input_coordinate_system=cyx_cs, output_coordinate_system=cyx_cs)
    affine = sequence.to_affine()
    matrix = affine.affine
    # bug, will be fixed soon
    matrix[0, 0] = 1.0
    print("matrix")
    print(matrix)
    print("inverse matrix")
    inverse_matrix = affine.inverse().to_affine().affine
    print(inverse_matrix)

    # predict shape
    x = im.shape[2]
    y = im.shape[1]
    v = np.array([[0, 0, 0, 1], [0, 0, x, 1], [0, y, 0, 1], [0, y, x, 1]])
    print("v")
    print(v)

    new_v = inverse_matrix @ v.T
    print("new v")
    print(new_v)

    new_y = np.max(new_v[1, :])
    new_x = np.max(new_v[2, :])
    print(f"new_y = {new_y}, new_x = {new_x}")

    ##
    scaled = dask_image.ndinterp.affine_transform(im.data, matrix, output_shape=(im.shape[0], int(new_y), int(new_x)))
    scaled = scaled[1:2, :, :]
    # scaled *= 255. / scaled.max()
    scaled_parsed = sd.Image2DModel.parse(scaled, multiscale_factors=[2, 4, 8])

    PLOT = False
    if PLOT:
        a = scaled_parsed["scale2"]["image"]
        a.plot()
        plt.show()

    ##
    start = time.time()
    sdata.add_image("scaled1", scaled_parsed, overwrite=True)
    print(f"saving: {time.time() - start}")
