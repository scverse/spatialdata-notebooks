##
import shutil
from typing import Optional
import hashlib
import os
import zipfile
import PIL
import json
import numpy as np
import pandas as pd

PIL.Image.MAX_IMAGE_PIXELS = None
from dask_image.imread import imread
from spatialdata._core.models import Image2DModel, ShapesModel, TableModel
from spatialdata._core.core_utils import _get_transformations, _set_transformations, SpatialElement
from spatialdata._core.transformations import Identity, Affine, Sequence, Scale, BaseTransformation
from spatialdata import SpatialData
from napari_spatialdata import Interactive
from spatial_image import SpatialImage
from anndata import AnnData
from spatialdata_io.readers._utils._read_10x_h5 import _read_10x_h5


##
path = os.path.join("data/lundeberg/", "svw96g68dv-1.zip")
OUT_FOLDER = os.path.join("data/lundeberg/", "converted")
os.makedirs(OUT_FOLDER, exist_ok=True)
SDATA_SMALL_IMAGES = os.path.join(OUT_FOLDER, "small_images.zarr")
SDATA_LARGE_IMAGES_PATIENT1_VISIUM = os.path.join(OUT_FOLDER, "large_images_patient1_visium.zarr")
SDATA_LARGE_IMAGES_PATIENT2_VISIUM = os.path.join(OUT_FOLDER, "large_images_patient2_visium.zarr")
SDATA_LARGE_IMAGES_PATIENT1_1K = os.path.join(OUT_FOLDER, "large_images_patient1_1k.zarr")
SDATA_EXPRESSION_PATIENT1_VISIUM_PATH = os.path.join(OUT_FOLDER, "expression_patient1_visium.zarr")
SDATA_EXPRESSION_PATIENT2_VISIUM_PATH = os.path.join(OUT_FOLDER, "expression_patient2_visium.zarr")
SDATA_EXPRESSION_PATIENT1_1K_PATH = os.path.join(OUT_FOLDER, "expression_patient1_1k.zarr")
##
# unzip the data
unzipped_path = path.replace(".zip", "")
UNZIP = False
if UNZIP:
    # please manually download the data from https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com
    # /svw96g68dv-1.zip
    CHECKSUM = "eebd948d752a6d16b9c972e3fc4b293c4fa0fc16edbcbec41c8c5d48acf2143b"

    assert os.path.isfile(path)
    if hashlib.sha256(open(path, "rb").read()).hexdigest() != CHECKSUM:
        print("checksum mismatch")
    else:
        print("checksum ok")

    if not os.path.exists(unzipped_path):
        print("Unzipping the data")
        with zipfile.ZipFile(path) as zip_ref:
            zip_ref.extractall(os.path.dirname(unzipped_path))
        print("data unzipped")
    assert os.path.isdir(unzipped_path)
##
SAVE_IMAGES = False
if SAVE_IMAGES:
    os.listdir(unzipped_path)
    paths_patient1_visium = {
        "sample_overview_patient1_visium": os.path.join(
            unzipped_path,
            "Additional_figures/Prostate_Patient_1.png",
        ),
        "schematic_overview_patient1_visium": os.path.join(
            unzipped_path, "Additional_figures/Spatial_GEFs_Patient_1_Visium.png"
        ),
    }
    paths_patient2_visium = {
        "sample_overview_patient2_visium": os.path.join(
            unzipped_path,
            "Additional_figures/Prostate_Patient_2.png",
        ),
        "schematic_overview_patient2_visium": os.path.join(
            unzipped_path, "Additional_figures/Spatial_GEFs_Patient_2_Visium.png"
        ),
    }
    paths_patient1_1k = {
        "schematic_overview_patient1_1k": os.path.join(
            unzipped_path,
            "Additional_figures/Spatial_GEFs_Patient_1_1k.png",
        ),
    }
    ##
    images = {}

    def _parse_image(path: str, sample_name: str) -> SpatialImage:
        image = Image2DModel.parse(imread(path).squeeze(), dims=("y", "x", "c"), multiscale_factors=[2, 2, 2, 2])
        d = _get_transformations(image)
        d[sample_name] = d["global"]
        del d["global"]
        _set_transformations(image, d)
        return image

    for name, path in paths_patient1_visium.items():
        images[name] = _parse_image(path, sample_name="patient1_visium")
    for name, path in paths_patient2_visium.items():
        images[name] = _parse_image(path, sample_name="patient2_visium")
    for name, path in paths_patient1_1k.items():
        images[name] = _parse_image(path, sample_name="patient1_1k")

    im = images["sample_overview_patient1_visium"]
    d = _get_transformations(im)
    d["patient1_1k"] = Identity()

    sdata_small_images = SpatialData(images=images)
    sdata_small_images.write(SDATA_SMALL_IMAGES)
    ##
    print("Converting large images (patient 1 Visium)")
    large_images_patient1_visium = {}
    for name in os.listdir(os.path.join(unzipped_path, "Histological_images/Patient_1/Visium/")):
        if name.endswith(".jpg"):
            path = os.path.join(unzipped_path, "Histological_images/Patient_1/Visium/", name)
            large_images_patient1_visium[name.replace(".jpg", "") + "_patient1_visium"] = _parse_image(
                path, sample_name=name.replace(".jpg", "") + "_patient1_visium"
            )
    sdata_large_images_patient1_visium = SpatialData(images=large_images_patient1_visium)
    sdata_large_images_patient1_visium.write(SDATA_LARGE_IMAGES_PATIENT1_VISIUM)
    ##
    print("Converting large images (patient 2 Visium)")
    large_images_patient2_visium = {}
    for name in os.listdir(os.path.join(unzipped_path, "Histological_images/Patient_2/")):
        if name.endswith(".jpg"):
            path = os.path.join(unzipped_path, "Histological_images/Patient_2/", name)
            large_images_patient2_visium[name.replace(".jpg", "") + "_patient2_visium"] = _parse_image(
                path, sample_name=name.replace(".jpg", "") + "_patient2_visium"
            )
    sdata_large_images_patient2_visium = SpatialData(images=large_images_patient2_visium)
    sdata_large_images_patient2_visium.write(SDATA_LARGE_IMAGES_PATIENT2_VISIUM)
    ##
    print("Converting large images (patient 1 1k)")
    large_images_patient1_1k = {}
    for name in os.listdir(os.path.join(unzipped_path, "Histological_images/Patient_1/1k-array/")):
        if name.endswith(".jpg"):
            path = os.path.join(unzipped_path, "Histological_images/Patient_1/1k-array/", name)
            large_images_patient1_1k[name.replace(".jpg", "") + "_patient1_1k"] = _parse_image(
                path, sample_name=name.replace(".jpg", "") + "_patient1_1k"
            )
    sdata_large_images_patient1_1k = SpatialData(images=large_images_patient1_1k)
    sdata_large_images_patient1_1k.write(SDATA_LARGE_IMAGES_PATIENT1_1K)
    ##

##
def merge_tables(tables: list[AnnData]) -> Optional[AnnData]:
    if len(tables) == 0:
        return None
    if len(tables) == 1:
        return tables[0]

    # not all tables can be merged, they need to have compatible region, region_key and instance_key values
    MERGED_TABLES_REGION_KEY = "annotated_element_merged"
    for table in tables:
        assert MERGED_TABLES_REGION_KEY not in table.obs

    spatialdata_attrs_found = [TableModel.ATTRS_KEY in table.uns for table in tables]
    assert all(spatialdata_attrs_found) or not any(spatialdata_attrs_found)
    if not any(spatialdata_attrs_found):
        merged_region = None
        merged_region_key = None
        merged_instance_key = None
    else:
        all_instance_keys = [table.uns[TableModel.ATTRS_KEY][TableModel.INSTANCE_KEY] for table in tables]
        assert all(all_instance_keys[0] == instance_key for instance_key in all_instance_keys)
        merged_instance_key = all_instance_keys[0]

        all_region_keys = []
        for table in tables:
            region = table.uns[TableModel.ATTRS_KEY][TableModel.REGION_KEY]
            region_key = table.uns[TableModel.ATTRS_KEY][TableModel.REGION_KEY_KEY]
            assert (
                isinstance(region, str)
                and region_key is None
                or isinstance(region, list)
                and isinstance(region_key, str)
            )
            if isinstance(region, list):
                all_region_keys.append(region_key)
            else:
                assert (
                    len(all_region_keys) == 0
                    or len(set(all_region_keys)) == 1
                    and all_region_keys[0] == MERGED_TABLES_REGION_KEY
                )
                table.obs[MERGED_TABLES_REGION_KEY] = region
                all_region_keys.append(MERGED_TABLES_REGION_KEY)
        assert len(set(all_region_keys)) == 1
        merged_region_key = all_region_keys[0]

        all_regions = []
        for table in tables:
            region = table.uns[TableModel.ATTRS_KEY][TableModel.REGION_KEY]
            if isinstance(region, str):
                all_regions.append(region)
            else:
                all_regions.extend(region)
        assert len(all_regions) == len(set(all_regions))
        merged_region = all_regions

    # print(merged_region)
    # print(merged_region_key)
    # print(merged_instance_key)

    attr = {"region": merged_region, "region_key": merged_region_key, "instance_key": merged_instance_key}
    merged_table = AnnData.concatenate(*tables, join="outer", uns_merge="same")

    # remove the MERGED_TABLES_REGION_KEY column if it has been added (the code above either adds that column
    # to all the tables, either it doesn't add it at all)
    for table in tables:
        if MERGED_TABLES_REGION_KEY in table.obs:
            del table.obs[MERGED_TABLES_REGION_KEY]

    merged_table.uns[TableModel.ATTRS_KEY] = attr
    # print(merged_table.uns)
    merged_table.obs[merged_region_key] = merged_table.obs[merged_region_key].astype("category")
    TableModel().validate(merged_table)
    return merged_table


##


sdata_small_images = SpatialData.read(SDATA_SMALL_IMAGES)
sdata_large_images_patient1_visium = SpatialData.read(SDATA_LARGE_IMAGES_PATIENT1_VISIUM)
sdata_large_images_patient2_visium = SpatialData.read(SDATA_LARGE_IMAGES_PATIENT2_VISIUM)
sdata_large_images_patient1_1k = SpatialData.read(SDATA_LARGE_IMAGES_PATIENT1_1K)

PARSE_VISIUM_DATA = False
if PARSE_VISIUM_DATA:
    ##
    VISIUM_FOLDER_PATIENT1 = os.path.join(unzipped_path, "Count_matrices/Patient 1/Visium_with_annotation/")
    VISIUM_FOLDER_PATIENT2 = os.path.join(unzipped_path, "Count_matrices/Patient_2/")
    # these values are the same that I have hardcoded in the function is_excluded() below
    excluded_patient1 = set(os.listdir(VISIUM_FOLDER_PATIENT1)).symmetric_difference(
        set(name.replace("_patient1_visium", "") for name in sdata_large_images_patient1_visium.images.keys())
    )
    excluded_patient2 = set(os.listdir(VISIUM_FOLDER_PATIENT2)).symmetric_difference(
        set(name.replace("_patient2_visium", "") for name in sdata_large_images_patient2_visium.images.keys())
    )

    def parse_visium_data(suffix, folder) -> tuple[dict[str, AnnData], AnnData]:
        shapes = {}
        tables = {}
        for name in os.listdir(folder):
            ##
            DATASET_PATH = os.path.join(folder, name)

            COUNTS_MATRIX_PATH = os.path.join(DATASET_PATH, "filtered_feature_bc_matrix.h5")
            SCALE_FACTOR_JSON_PATH = os.path.join(DATASET_PATH, "scalefactors_json.json")
            TISSUE_POSITIONS_PATH = os.path.join(DATASET_PATH, "tissue_positions_list.csv")
            ANNOTATIONS_PATH = os.path.join(DATASET_PATH, f"{name}_Final_Consensus_Annotations.csv")

            assert os.path.isfile(COUNTS_MATRIX_PATH)
            assert os.path.isfile(SCALE_FACTOR_JSON_PATH)
            assert os.path.isfile(TISSUE_POSITIONS_PATH)

            # expression data
            adata = _read_10x_h5(COUNTS_MATRIX_PATH)
            adata.obs["visium_spot_id"] = adata.obs_names
            table = TableModel.parse(
                adata, region=f"/shapes/{name}{suffix}", region_key=None, instance_key="visium_spot_id"
            )
            # table.obs.reset_index(inplace=True)
            # table.obs.index = table.obs.index.astype(str)
            table.var_names_make_unique()

            # scale factors
            with open(SCALE_FACTOR_JSON_PATH, "r") as infile:
                scalefactors = json.load(infile)

            # circles coordinates
            df = pd.read_csv(TISSUE_POSITIONS_PATH, header=None, index_col=0)
            df = df[df.index.isin(adata.obs_names)]
            coords = df.iloc[:, np.array([4, 3])].values
            # if we don't remove the index name the writing to zarr fails (the index name is the int 0, maybe converting it to str would also work)
            df.rename_axis(None, inplace=True)

            if suffix == "_patient1_visium":
                transformation = Identity()
            elif suffix == "_patient2_visium":
                transformation = Scale([0.5, 0.5], axes=("x", "y"))
            else:
                raise ValueError(f"Unknown suffix: {suffix}")
            circles = ShapesModel.parse(
                coords,
                shape_type="Circle",
                shape_size=scalefactors["spot_diameter_fullres"],
                index=df.index,
                transformations={f"{name}{suffix}": transformation},
            )
            shapes[f"{name}{suffix}"] = circles

            # cell-type annotations, if available (only for patient 1)
            if suffix == "_patient1_visium":
                assert os.path.isfile(ANNOTATIONS_PATH)
                annotations = pd.read_csv(ANNOTATIONS_PATH, index_col=0)
                annotations["Final_Annotations"] = annotations["Final_Annotations"].fillna("")
                annotations["Final_Annotations"] = annotations["Final_Annotations"].astype("str").astype("category")
                table.obs["Final_Annotations"] = annotations["Final_Annotations"]

            tables[f"{name}{suffix}"] = table
        tables = list(tables.values())

        table = merge_tables(tables)
        return shapes, table
        ##

    shapes_patient1_visium, table_patient1_visium = parse_visium_data(
        suffix="_patient1_visium", folder=VISIUM_FOLDER_PATIENT1
    )
    sdata_expression_patient1_visium = SpatialData(shapes=shapes_patient1_visium, table=table_patient1_visium)
    if os.path.isdir(SDATA_EXPRESSION_PATIENT1_VISIUM_PATH):
        shutil.rmtree(SDATA_EXPRESSION_PATIENT1_VISIUM_PATH)
    sdata_expression_patient1_visium.write(SDATA_EXPRESSION_PATIENT1_VISIUM_PATH)

    shapes_patient2_visium, table_patient2_visium = parse_visium_data(
        suffix="_patient2_visium", folder=VISIUM_FOLDER_PATIENT2
    )
    sdata_expression_patient2_visium = SpatialData(shapes=shapes_patient2_visium, table=table_patient2_visium)
    if os.path.isdir(SDATA_EXPRESSION_PATIENT2_VISIUM_PATH):
        shutil.rmtree(SDATA_EXPRESSION_PATIENT2_VISIUM_PATH)
    sdata_expression_patient2_visium.write(SDATA_EXPRESSION_PATIENT2_VISIUM_PATH)
# some images are not aligned to the reference (they are not present in the alignment drawings)
def is_exlcuded(name: str):
    excluded_names = (
        [s + "_patient1_visium" for s in ["V1_1", "H1_1"]]
        + [
            s + "_patient2_visium"
            for s in [
                "H1_1",
                "H1_2",
                "H1_3",
                "H1_4",
                "H2_3",
                "H2_4",
                "H2_5",
                "H2_6",
                "H3_3",
                "V2_3",
                "V2_4",
                "V2_5",
                "V2_6",
            ]
        ]
        + [s + "_patient1_1k" for s in []]
    )
    if name in excluded_names:
        return True
    return False


##
sdata_expression_patient1_visium = SpatialData.read(SDATA_EXPRESSION_PATIENT1_VISIUM_PATH)
sdata_expression_patient2_visium = SpatialData.read(SDATA_EXPRESSION_PATIENT2_VISIUM_PATH)

##
def map_elements(
    references_coords: AnnData,
    moving_coords: AnnData,
    reference_element: SpatialElement,
    moving_element: SpatialElement,
    sdata: Optional[SpatialData] = None,
    reference_coordinate_system: str = "global",
    moving_coordinate_system: str = "global",
    new_coordinate_system: Optional[str] = None,
) -> tuple[BaseTransformation, BaseTransformation]:
    from skimage.transform import estimate_transform

    model = estimate_transform("affine", src=moving_coords.obsm["spatial"], dst=references_coords.obsm["spatial"])
    transform_matrix = model.params
    a = transform_matrix[:2, :2]
    d = np.linalg.det(a)
    # print(d)
    if d < 0:
        m = (moving_coords.obsm["spatial"][:, 0].max() - moving_coords.obsm["spatial"][:, 0].min()) / 2
        flip = Affine(
            np.array(
                [
                    [-1, 0, 2 * m],
                    [0, 1, 0],
                    [0, 0, 1],
                ]
            ),
            input_axes=("x", "y"),
            output_axes=("x", "y"),
        )
        flipped_moving_coords = flip.transform(moving_coords)
        model = estimate_transform(
            "similarity", src=flipped_moving_coords.obsm["spatial"], dst=references_coords.obsm["spatial"]
        )
        final = Sequence([flip, Affine(model.params, input_axes=("x", "y"), output_axes=("x", "y"))])
    else:
        model = estimate_transform(
            "similarity", src=moving_coords.obsm["spatial"], dst=references_coords.obsm["spatial"]
        )
        final = Affine(model.params, input_axes=("x", "y"), output_axes=("x", "y"))

    affine = Affine(
        final.to_affine_matrix(input_axes=("x", "y"), output_axes=("x", "y")),
        input_axes=("x", "y"),
        output_axes=("x", "y"),
    )

    # get the old transformations of the visium and xenium data
    old_moving_transformation = SpatialData.get_transformation(moving_element, moving_coordinate_system)
    old_reference_transformation = SpatialData.get_transformation(reference_element, reference_coordinate_system)

    # compute the new transformations
    new_moving_transformation = Sequence([old_moving_transformation, affine])
    new_reference_transformation = old_reference_transformation

    if new_coordinate_system is not None:
        # this allows to work on singleton objects, not embedded in a SpatialData object
        set_transform = sdata.set_transformation if sdata is not None else SpatialData.set_transformation_in_memory
        set_transform(moving_element, new_moving_transformation, new_coordinate_system)
        set_transform(reference_element, new_reference_transformation, new_coordinate_system)
    return new_moving_transformation, new_reference_transformation


##
def manually_annotate_landmarks(big_images_sdata, suffix):
    small_image_overview = sdata_small_images.images[f"schematic_overview{suffix}"]
    # i = 0
    empty_shapes = np.array([[10, 0]])
    # can't make an empty adata (TODO: support), it breaks the parser or napari
    empty_adata = ShapesModel.parse(coords=empty_shapes, shape_type="Circle", shape_size=10)
    for name in big_images_sdata.images.keys():
        if name.endswith(suffix):
            if is_exlcuded(name):
                continue
            # i += 1
            # if i > 2:
            #     break
            merged = SpatialData(images={"overview": small_image_overview, name: big_images_sdata.images[name]})
            merged.add_shapes(name=name + "_source", shapes=empty_adata.copy())
            merged.add_shapes(name=name + "_target", shapes=empty_adata.copy())
            Interactive(merged)
            landmarks = SpatialData(shapes=merged.shapes)
            ##
            # to remove the first coordinate pair coming from "empty_shapes"
            keys = list(landmarks.shapes.keys())
            for k in keys:
                v = landmarks.shapes[k]
                if len(v) == 4:
                    new_v = v[1:, :].copy()
                    landmarks.add_shapes(name=k, shapes=new_v, overwrite=True)
            ##
            landmarks.write(os.path.join(OUT_FOLDER, f"landmarks_{name}.zarr"), overwrite=True)


ANNOTATE_LANDMARKS = False
if ANNOTATE_LANDMARKS:
    pass
    # manually_annotate_landmarks(big_images_sdata=sdata_large_images_patient1_visium, suffix="_patient1_visium")
    # manually_annotate_landmarks(big_images_sdata=sdata_large_images_patient2_visium, suffix="_patient2_visium")
    # manually_annotate_landmarks(big_images_sdata=sdata_large_images_patient1_1k, suffix="_patient1_1k")

##


def align_using_landmakrs(merged_sdata, big_images_sdata, suffix):
    small_image_overview = sdata_small_images.images[f"schematic_overview{suffix}"]
    i = 0
    for name in big_images_sdata.images.keys():
        if name.endswith(suffix):
            if is_exlcuded(name):
                continue
            # i += 1
            # if i > 2:
            #     break
            landmarks = SpatialData.read(os.path.join(OUT_FOLDER, f"landmarks_{name}.zarr"))
            map_elements(
                references_coords=landmarks.shapes[name + "_target"],
                moving_coords=landmarks.shapes[name + "_source"],
                reference_element=small_image_overview,
                moving_element=merged_sdata.images[name],
                sdata=merged_sdata,
                reference_coordinate_system=suffix[1:],
                moving_coordinate_system=name,
                new_coordinate_system=suffix[1:],
            )
            # the data
            map_elements(
                references_coords=landmarks.shapes[name + "_target"],
                moving_coords=landmarks.shapes[name + "_source"],
                reference_element=small_image_overview,
                moving_element=merged_sdata.shapes[name],
                sdata=merged_sdata,
                reference_coordinate_system=suffix[1:],
                moving_coordinate_system=name,
                new_coordinate_system=suffix[1:],
            )
            pass


##

##
# patient1_visium
sdata_patient1_visium = SpatialData(
    images={
        **sdata_small_images.images,
        **sdata_large_images_patient1_visium.images,
    },
    shapes=sdata_expression_patient1_visium.shapes,
    table=sdata_expression_patient1_visium.table,
)
keys = list(sdata_patient1_visium.images.keys())
for name in keys:
    if is_exlcuded(name):
        if name in sdata_patient1_visium.images:
            print(f"deleting {name}")
            del sdata_patient1_visium.images[name]

align_using_landmakrs(
    merged_sdata=sdata_patient1_visium, big_images_sdata=sdata_large_images_patient1_visium, suffix="_patient1_visium"
)

##
sdata_patient1_visium.table.obs["Final_Annotations"] = sdata_patient1_visium.table.obs["Final_Annotations"].astype(
    "category"
)

##
# patient2_visium (copying the code above)
sdata_patient2 = SpatialData(
    images={
        **sdata_small_images.images,
        **sdata_large_images_patient2_visium.images,
    },
    shapes=sdata_expression_patient2_visium.shapes,
    table=sdata_expression_patient2_visium.table,
)
keys = list(sdata_patient2.images.keys())
for name in keys:
    if is_exlcuded(name):
        if name in sdata_patient2.images:
            print(f"deleting {name}")
            del sdata_patient2.images[name]
align_using_landmakrs(
    merged_sdata=sdata_patient2, big_images_sdata=sdata_large_images_patient2_visium, suffix="_patient2_visium"
)
##
# align_using_landmakrs(big_images_sdata=sdata_large_images_patient1_1k, suffix="_patient1_1k")
##

# from itertools import islice
# sdata_patient1_visium._shapes = dict(list(islice(sdata_patient1_visium.shapes.items(), 2)))
# TODO: this should have been categorical! Not sure why it's object now. Maybe it is a bug with the IO. This has to be fixed otherwise napari can't
# display the categorical data with the consistent colors among subsets of the table
# Interactive(sdata_patient1_visium)
# Interactive(sdata_patient2)
##
# Interactive(sdata_small_images)
##
ALIGN_SMALL_IMAGES = False
if ALIGN_SMALL_IMAGES:
    ANNOTATE_LANDMARKS = False
    if ANNOTATE_LANDMARKS:
        sdata_anchor_points_between_schematics_patient1 = SpatialData(shapes=sdata_small_images.shapes)
        sdata_anchor_points_between_schematics_patient1.write(
            os.path.join(OUT_FOLDER, "sdata_anchor_points_between_schematics_patient1.zarr")
        )
    sdata_anchor_points_between_schematics_patient1 = SpatialData.read(
        os.path.join(OUT_FOLDER, "sdata_anchor_points_between_schematics_patient1.zarr")
    )
    moving = sdata_anchor_points_between_schematics_patient1.shapes["moving"]
    reference = sdata_anchor_points_between_schematics_patient1.shapes["reference"]
    map_elements(
        references_coords=reference,
        moving_coords=moving,
        reference_element=sdata_small_images.images["schematic_overview_patient1_visium"],
        moving_element=sdata_small_images.images["schematic_overview_patient1_1k"],
        sdata=sdata_small_images,
        reference_coordinate_system="patient1_visium",
        moving_coordinate_system="patient1_1k",
        new_coordinate_system="patient1_1k_aligned",
    )
    Interactive(sdata_small_images)
##
# add 1k expression data
PARSE_1K_DATA = False
if PARSE_1K_DATA:
    ##
    ONE_K_FOLDER_PATIENT1 = os.path.join(unzipped_path, "Count_matrices/Patient 1/1k_arrays/")
    suffix = "_patient1_1k"

    shapes = {}
    tables = {}
    # i = 0
    # name = os.listdir(ONE_K_FOLDER_PATIENT1)[0]
    for name in os.listdir(ONE_K_FOLDER_PATIENT1):
        # i += 1
        # if i > 2:
        #     break
        DATASET_PATH = os.path.join(ONE_K_FOLDER_PATIENT1, name)
        files = os.listdir(DATASET_PATH)
        assert len(files) == 2
        expression_data_file = [f for f in files if f.endswith("_stdata.tsv")][0]
        positions_file = [f for f in files if not f.endswith("_stdata.tsv")][0]
        print(
            "patient1_1k, name = ",
            name,
            ", expression_data_file = ",
            expression_data_file,
            ", positions_file = ",
            positions_file,
            sep="",
        )

        expression = pd.read_csv(os.path.join(DATASET_PATH, expression_data_file), sep="\t", index_col=0)
        positions = pd.read_csv(os.path.join(DATASET_PATH, positions_file), sep="\t", index_col=None)
        positions["combined_name"] = positions[["x", "y"]].apply(lambda x: f"{x['x']}x{x['y']}", axis=1)
        merged = pd.merge(positions, expression, left_on="combined_name", right_index=True, how="inner")
        positions_filtered = merged[positions.columns].copy()
        expression_filtered = merged[expression.columns].copy()

        adata = AnnData(expression_filtered)
        adata.obs["combined_name"] = positions_filtered["combined_name"].to_numpy()
        # print(adata.obs['combined_name'])
        assert adata.obs["combined_name"].is_unique
        table = TableModel.parse(adata, region=f"/shapes/{name}{suffix}", region_key=None, instance_key="combined_name")
        table.var_names_make_unique()
        tables[f"{name}{suffix}"] = table

        coords = positions_filtered[["pixel_x", "pixel_y"]].values
        circles = ShapesModel.parse(
            coords,
            shape_type="Circle",
            shape_size=100,
            index=adata.obs["combined_name"],
            transformations={f"{name}{suffix}": Identity()},
        )
        shapes[f"{name}{suffix}"] = circles
    table = merge_tables(list(tables.values()))
    ##
    sdata_expression_patient1_1k = SpatialData(shapes=shapes, table=table)
    if os.path.isdir(SDATA_EXPRESSION_PATIENT1_1K_PATH):
        shutil.rmtree(SDATA_EXPRESSION_PATIENT1_1K_PATH)
    sdata_expression_patient1_1k.write(SDATA_EXPRESSION_PATIENT1_1K_PATH)
    # Interactive(sdata_expression_patient1_1k)
##
sdata_expression_patient1_1k = SpatialData.read(SDATA_EXPRESSION_PATIENT1_1K_PATH)
sdata_patient1_1k = SpatialData(
    images={
        **sdata_small_images.images,
        **sdata_large_images_patient1_1k.images,
    },
    shapes=sdata_expression_patient1_1k.shapes,
    table=sdata_expression_patient1_1k.table,
)
ALIGN_MAPPING_BETWEEN_1K_IMAGE_AND_EXPRESSION = True
if ALIGN_MAPPING_BETWEEN_1K_IMAGE_AND_EXPRESSION:
    WRITE = False
    if WRITE:
        Interactive(sdata_patient1_1k)
        moving = sdata_patient1_1k.shapes["moving"]
        reference = sdata_patient1_1k.shapes["reference"]
        sdata_mapping_between_1k_image_and_expression = SpatialData(shapes={"moving": moving, "reference": reference})
        sdata_mapping_between_1k_image_and_expression.write(
            os.path.join(OUT_FOLDER, "sdata_mapping_between_1k_image_and_expression_patient1.zarr")
        )
    ##
    sdata_mapping_between_1k_image_and_expression = SpatialData.read(
        os.path.join(OUT_FOLDER, "sdata_mapping_between_1k_image_and_expression_patient1.zarr")
    )
    for name, shapes in sdata_patient1_1k.shapes.items():
        if name.endswith("_patient1_1k"):
            image = sdata_patient1_1k.images[name]
            moving_transformation, _ = map_elements(
                references_coords=sdata_mapping_between_1k_image_and_expression.shapes["reference"],
                moving_coords=sdata_mapping_between_1k_image_and_expression.shapes["moving"],
                reference_element=image,
                moving_element=shapes,
                sdata=None,
                reference_coordinate_system=name,
                moving_coordinate_system=name,
                new_coordinate_system=None,
            )
            sdata_patient1_1k.set_transformation(
                sdata_patient1_1k.shapes[name],
                moving_transformation,
                target_coordinate_system=name,
            )
    print(sdata_patient1_1k)
    # Interactive(sdata_patient1_1k)
    ##

pass
pass
# TODO: refine the alignemnt of the visium data (patient 1 and 2) to the schematics. Needs points to be implemented back (because we need those, we can't use shapes anymore)
# TODO: refine the alignemnt of the 1k expression to the images
# TODO: make the aligment of the 1k data to the schematics
# TODO: refine the alignment of the 1k data to the schematics

# note: I could not deduce how the following images are aligned to the schematic from the paper (patient 1, 1k): H1_2, H2_1, H2_2, H2_5, V1_1, V1_3, V2_6
ANNOTATE_LANDMARKS = True
if ANNOTATE_LANDMARKS:
    manually_annotate_landmarks(big_images_sdata=sdata_large_images_patient1_1k, suffix="_patient1_1k")
