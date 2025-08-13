from spatialdata.transformations import Affine
from spatialdata import SpatialData
from spatialdata.transformations import (
    BaseTransformation,
    Sequence,
    get_transformation,
    set_transformation,
)


AFFINE_VISIUM_XENIUM = Affine(
    [
        [1.61711846e-01, 2.58258090e00, -1.24575040e04],
        [-2.58258090e00, 1.61711846e-01, 3.98647301e04],
        [0.0, 0.0, 1.0],
    ],
    input_axes=("x", "y"),
    output_axes=("x", "y"),
)


def postpone_transformation(
    sdata: SpatialData,
    transformation: BaseTransformation,
    source_coordinate_system: str,
    target_coordinate_system: str,
):
    for element_type, element_name, element in sdata._gen_elements():
        old_transformations = get_transformation(element, get_all=True)
        if source_coordinate_system in old_transformations:
            old_transformation = old_transformations[source_coordinate_system]
            sequence = Sequence([old_transformation, transformation])
            set_transformation(element, sequence, target_coordinate_system)
