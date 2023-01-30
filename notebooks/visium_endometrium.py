##
# data from endometrium sample, described here https://pubmed.ncbi.nlm.nih.gov/34857954/
import os
import shutil
import time
from pathlib import Path

import numpy as np
import spatialdata as sd
import xarray as xr
from napari_spatialdata import Interactive
from PIL import Image
from spatialdata_io import read_visium
from tqdm.notebook import tqdm

##
# luca's workaround for pycharm
path = Path().resolve()
if str(path).endswith("spatialdata-io/src"):
    os.chdir(path.parent.parent / "spatialdata-notebooks")

##
root = "local_data/visium_endometrium/raw/"
processed = "local_data/visium_endometrium/processed/"
zarr_path = os.path.join(processed, "data.zarr")
assert os.path.isdir(root), os.getcwd()
os.makedirs(processed, exist_ok=True)

##
samples = ["152806", "152807", "152810", "152811"]
# samples = ["152806"]

##
sdatas = []
for sample in tqdm(samples):
    spaceranger_data = os.path.join(root, "visium", sample)
    sdata = read_visium(spaceranger_data, coordinate_system_name=sample)
    print(sdata)
    sdatas.append(sdata)

sdata = sd.SpatialData.concatenate(sdatas)
print(sdata)

##
if os.path.isdir(zarr_path):
    shutil.rmtree(zarr_path)
sdata.write(zarr_path)
#
# ##
sdata0 = sdata.filter_by_coordinate_system(samples[0])
print(sdata0)
print(sdatas[0])

# ##
# # interactive = Interactive(sdata=sdata)
#
##
Image.MAX_IMAGE_PIXELS = 5000000000


def get_hires_img(sample):  # noqa: D103
    f = os.path.join(root, "hires_images")
    if sample == "152810":
        res = "20x"
    else:
        res = "40x"
    path = os.path.join(f, f"{sample}_{res}_highest_res_image.jpg")
    # print(path)
    im = Image.open(path)
    start = time.time()
    img = xr.DataArray(im, dims=("y", "x", "c"))
    print(f"loading image: {time.time() - start}")
    # start = time.time()
    # assert img.dtype == np.float32
    # assert img.min() >= 0. and img.max() <= 1.
    # img = (img * 255).astype(np.uint8)
    # print(f'converting to uint8: {time.time() - start}')
    return img


for sample in tqdm(samples, desc="large images"):
    img = get_hires_img(sample)
    assert img.dtype == np.uint8

    from spatialdata import Identity
    from spatialdata._core.elements import Image as ImageElement

    cs = sdata.coordinate_systems[sample]
    image = ImageElement(img.transpose("c", "y", "x"), alignment_info={cs: Identity()})
    name = f"hires_{sample}"
    sdata.images[name] = image
    start = time.time()
    sdata._save_element("images", name, path=zarr_path)
    print(f"saving image: {time.time() - start}")
##
sdata = sd.SpatialData.read(zarr_path)

for sample in samples:
    if sample == "152806":
        source_points = np.array([[19465, 50704], [36663, 12568]])
        target_points = np.array([[597, 1718], [1164, 462]])
    elif sample == "152807":
        source_points = np.array([[4675, 19252], [26610, 36954]])
        target_points = np.array([[172, 695], [913, 1294]])
    elif sample == "152810":
        source_points = np.array([[2945, 10284], [17174, 23167]])
        target_points = np.array([[152, 730], [1090, 1579]])
    elif sample == "152811":
        source_points = np.array([[29704, 41867], [4809, 21925]])
        target_points = np.array([[1033, 1458], [190, 783]])
    else:
        raise ValueError()
    small_image_transformation = sdata.images[sample].transformations[sample]
    big_image_transformation = sd.Sequence(
        [
            sd.Affine(sd.Affine._get_affine_iniection_from_axes(src_axes=("c", "y", "x"), des_axes=("x", "y"))[:-1, :]),
            sd.Translation(-source_points[0, :]),
            sd.Scale((target_points[1, :] - target_points[0, :]) / (source_points[1, :] - source_points[0, :])),
            sd.Translation(target_points[0, :]),
            sd.Affine(sd.Affine._get_affine_iniection_from_axes(src_axes=("x", "y"), des_axes=("c", "y", "x"))[:-1, :]),
            small_image_transformation,
        ]
    )
    for t in big_image_transformation.transformations:
        print(t.to_affine().affine)
    print(big_image_transformation.to_affine().affine)
    sdata.images[f"hires_{sample}"].transformations[sample] = big_image_transformation
    # del sdata.images[f'hires_{sample}']
##
interactive = Interactive(sdata=sdata)
# print(sdata)

# def add_cell2location_data():
#     cell2location_data_folder = os.path.join(
#         root,
#         "raw/visium/20201207_LocationModelLinearDependentWMultiExperiment_19clusters_20952locations_19980genes",
#     )
#     os.listdir(cell2location_data_folder)
#     f = os.path.join(cell2location_data_folder, "sp.h5ad")
#     import anndata as ad
#     import scanpy as sc
#
#     a = ad.read_h5ad(f)
#     ##
#     adatas = {}
#     for sample in samples:
#         ii = a.obs["sample"] == sample
#         aa = a[ii]
#         adatas[sample] = aa
#     ##
#     cell_types = [
#         "Endothelial ACKR1",
#         "Endothelial SEMA3G",
#         "Epithelial Ciliated",
#         "Epithelial Ciliated LRG5",
#         "Epithelial Glandular",
#         "Epithelial Glandular_secretory",
#         "Epithelial Lumenal 1",
#         "Epithelial Lumenal 2",
#         "Epithelial Pre-ciliated",
#         "Epithelial SOX9",
#         "Epithelial SOX9_LGR5",
#         "Fibroblast C7",
#         "Fibroblast dS",
#         "Fibroblast eS",
#         "Lymphoid",
#         "Myeloid",
#         "PV MYH11",
#         "PV STEAP4",
#         "uSMC",
#     ]
#     for sample in tqdm(samples):
#         for feature in ["mean_spot_factors", "mean_nUMI_factors"]:
#             s = get_smu_file(sample)
#             aa = adatas[sample]
#             spots = s["visium"]["expression"]
#             # print(f'len(aa) = {len(aa)}, len(spots.obs) = {len(spots.obs)}')
#             assert len(aa) == len(spots.obs)
#             original_labels = aa.obs["spot_id"].to_numpy()
#             smu_labels = spots.masks.masks_labels
#             s0 = set(original_labels)
#             s1 = set(smu_labels)
#             different = s0.symmetric_difference(s1)
#             assert len(different) == 0
#
#             columns = [f"{feature}{c}" for c in cell_types]
#
#             df = aa.obs[columns].copy()
#             df["original_label"] = original_labels
#             df.set_index(keys="original_label", inplace=True)
#
#             data_for_smu = df.loc[smu_labels]
#             import pandas as pd
#
#             obs = pd.DataFrame(index=original_labels)
#             var = pd.DataFrame({"channel_name": columns})
#             masks = s["visium"]["expression"].masks.clone()
#             smu_factors = spatialmuon.Regions(
#                 X=data_for_smu.to_numpy(),
#                 var=var,
#                 masks=masks,
#                 anchor=s["visium"]["expression"].anchor,
#             )
#             if feature in s["visium"]:
#                 del s["visium"][feature]
#             s["visium"][feature] = smu_factors
#
#             _, axes = plt.subplots(1, 2)
#             ch = f"{feature}Endothelial ACKR1"
#             s["visium"]["image"].plot(ax=axes[0])
#             smu_factors.plot(ch, ax=axes[0])
#             sc.pl.spatial(aa, color=ch, spot_size=100, ax=axes[1])
#             plt.show()
#             s.backing.close()
#         ##
