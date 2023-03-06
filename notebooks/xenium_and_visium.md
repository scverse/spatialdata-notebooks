---
jupyter:
    jupytext:
        text_representation:
            extension: .md
            format_name: markdown
            format_version: "1.3"
            jupytext_version: 1.14.4
    kernelspec:
        display_name: Python 3 (ipykernel)
        language: python
        name: python3
---

# Joint analysis of Xenium and Visium data

## Converting the raw data to Zarr

```python
import shutil
import numpy as np
import napari
import os
import spatialdata as sd
from spatialdata._core.core_utils import get_default_coordinate_system
from spatialdata._core.transformations import Affine, Sequence, Identity
from napari_spatialdata import Interactive
from spatialdata_io import xenium, visium
```

```python
# you can use symlinks to spatiald-sandbox reachable from the notebooks folder
SPATIALDATA_SANDBOX_PATH = "../data/spatialdata-sandbox"
# the raw data can be downloaded using the scripts from spatialdata-sandbox
XENIUM_RAW_DATA_PATH = os.path.join(
    SPATIALDATA_SANDBOX_PATH, "xenium_io/data/xenium/outs"
)
VISIUM_RAW_DATA_PATH = os.path.join(SPATIALDATA_SANDBOX_PATH, "xenium_io/data/visium")
# these two are the output of the scripts in spatialdata-sandbox, but we will recreate them in this notebook
XENIUM_SDATA_PATH = os.path.join(SPATIALDATA_SANDBOX_PATH, "xenium_io/data.zarr")
VISIUM_SDATA_PATH = os.path.join(SPATIALDATA_SANDBOX_PATH, "xenium_io/data_visium.zarr")
# this zarr file will be created in this notebook
LANDMARKS_SDATA_PATH = os.path.join(
    SPATIALDATA_SANDBOX_PATH, "xenium_io/landmarks.zarr"
)

assert os.path.isdir(XENIUM_RAW_DATA_PATH)
assert os.path.isdir(VISIUM_RAW_DATA_PATH)
```

```python
# if we already converted the data to zarr we can just read it
ALREADY_IN_ZARR = True
```

```python
if ALREADY_IN_ZARR:
    xenium_sdata = sd.read_zarr(XENIUM_SDATA_PATH)
else:
    # here we read the raw data into spatialdata objects
    print("reading the xenium data... ", end="")
    xenium_sdata = xenium(XENIUM_RAW_DATA_PATH)
    print("done")

    # for large datasets, like in this case, saving the data to zarr will automatically improve the performance of
    # downstream processing thanks to file backing and chunked data storage
    print("saving the xenium data to zarr... ", end="")
    xenium_sdata.write(XENIUM_SDATA_PATH, overwrite=True)
    print("done")

print(xenium_sdata)
```

```python
if ALREADY_IN_ZARR:
    visium_sdata = sd.read_zarr(VISIUM_SDATA_PATH)
else:
    print("reading the visium data... ", end="")
    visium_sdata = visium(VISIUM_RAW_DATA_PATH)
    print("done")

    print("saving the visium data to zarr... ", end="")
    visium_sdata.write(VISIUM_SDATA_PATH, overwrite=True)
    print("done")

print(visium_sdata)
```

## Interactive visualization

```python
# let's explore the data interactively with napari; down below are some screenshots of the viewer
Interactive(xenium_sdata)
```

Showing the whole field of view.

![Screenshot 2023-01-31 at 18.30.37 (3).png](attachment:531312ec-300b-45e3-80b1-9aeec1acc058.png)

The images are very high resolution. Showing a zoomed in portion with the overlay of nuclei and cell boundaries.

![Screenshot 2023-01-31 at 18.31.52 (3).png](attachment:8bde5b8c-8094-41b9-9770-374b3180d19b.png)

Showing the gene expression of ADAM9.

![Screenshot 2023-01-31 at 18.33.12 (3).png](attachment:94eb2f6d-955d-41d1-8ebd-e1bd353f1ddc.png)

```python
Interactive(visium_sdata)
```

Showing the whole field of view. Notices how the data is not aligned to the Xenium one.

![Screenshot 2023-01-31 at 18.57.39 (3).png](attachment:80d7a71a-0a1b-447a-b3be-a0fa92a521ff.png)

Showing the gene expression of ADAM9.

![Screenshot 2023-01-31 at 19.01.21 (3).png](attachment:cecb2c76-1097-4e4b-beca-332452e2a6d7.png)

## Spatially aligning the two datasets

```python
merged = sd.SpatialData(
    images={
        "xenium": xenium_sdata.images["morphology_mip"],
        "visium": visium_sdata.images["CytAssist_FFPE_Human_Breast_Cancer_full_image"],
    }
)
```

```python
Interactive(sdata=merged)
```

The images are not aligned.

![Screenshot 2023-01-31 at 19.09.04 (3).png](attachment:3b33966b-7912-41e2-a10f-2948dfb4b4d7.png)

To align them, let's select 3 landmarks points points for each image (we could select more points for more accuracy).

![visium_trimmed.gif](attachment:df85ebd9-0207-4ed5-9266-60476ba478de.gif)
![xenium_trimmed.gif](attachment:3975af6f-ccdb-4d7d-a81d-23db189e5170.gif)

```python
# the landmarks points are now accessible from Python
merged
```

```python
# let's save them to Zarr so that we can use in the future if needed
ALREADY_IN_ZARR = True
if ALREADY_IN_ZARR:
    landmarks_sdata = sd.read_zarr(LANDMARKS_SDATA_PATH)
else:
    landmarks_sdata = sd.SpatialData(shapes=merged.shapes)
    landmarks_sdata.write(LANDMARKS_SDATA_PATH)

print(landmarks_sdata)
```

```python
# let's compute the affine transformation to map the Visium image onto the Xenium one
points_reference = landmarks_sdata.shapes["xenium_landmarks"].obsm["spatial"]
points_moving = landmarks_sdata.shapes["visium_landmarks"].obsm["spatial"]
from skimage.transform import SimilarityTransform

model = SimilarityTransform(dimensionality=2)
model.estimate(points_moving, points_reference)
transform_matrix = model.params
print(transform_matrix)
```

```python
affine = Affine(transform_matrix, input_axes=("x", "y"), output_axes=("x", "y"))

# get the old transformations of the visium and xenium data
old_visium_transformation = merged.get_transformation(
    element=merged.images["visium"], target_coordinate_system="global"
)
old_xenium_transformation = merged.get_transformation(
    element=merged.images["xenium"], target_coordinate_system="global"
)

# compute the new transformations
new_visium_transformation = Sequence([old_visium_transformation, affine])
new_xenium_transformation = Identity()

# add the new transformations to the "merged" object, mapping to a new coordinate system
merged.set_transformation(
    element=merged.images["visium"],
    transformation=new_visium_transformation,
    target_coordinate_system="aligned",
)
merged.set_transformation(
    element=merged.images["xenium"],
    transformation=new_xenium_transformation,
    target_coordinate_system="aligned",
)
```

```python
Interactive(merged)
```

The two images are now aligned in the `aligned` coordinate system.

![trimmed_aligned.gif](attachment:7048ab4c-1b46-4868-aef6-e1bc11b8b2bc.gif)

The aligned images are still in the full resolution, and napari can be used to performantly visualize the data.

![zoom_detail_trimmed.gif](attachment:cc27c87a-aa6c-4e14-8b29-dd17d68ff0be.gif)

We now align the whole spatialdata object. We do this by declaring that the 'aligned' coordinate system can be obtained from the 'global' one via a transformation. This will be the identity for the Xenium data, and the previously computed affine transformation for the Visium data.

```python
# this code is not yet supported but it will in one of the next prs
#
# xenium_sdata.set_transformation('global', 'aligned', Identity())
# visium_sdata.set_transformation('global', 'aligned', new_visium_transformation)
```

Finally we visualize both the Xenium and Visum data together.

```python
# this code is not yet supported but it will in one of the next prs
#
# Interactive([visium_data, xenium_data])
```

## TODOs

-   [ ] show an example of applying the transformations to create new elements (e.g. create a rotated Visium image)
-   [ ] more powerfully:
    -   [ ] implement rasterize for vector data (using datashared) and resize for raster data
    -   [ ] create a transformed and downscaled version of the data
-   [ ] use this for doing feature aggregation from any layer to any layer
-   [ ] draw polygons, save them to disk and use them to aggregate from any layer
-   [ ] visualize multiple spatialdata objects (and tables) with napari

## Later

-   [ ] (waiting for Kevin) show an example of spatial cropping
