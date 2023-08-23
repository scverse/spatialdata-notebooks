# Examples covering the whole storage specification

This directory offers comprehensive resources for developers that want to interface their methods with the SpatialData format in a robust way.

## Why this repository
The file storage format adopted by SpatialData is built on top of the latest version of the well-documented [OME-NGFF specification](https://ngff.openmicroscopy.org/latest/index.html), but it also uses *some* less-documented features of the OME-NGFF specification that are still [under review](https://github.com/ome/ngff/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc), or experimental storage strategies that will be eventually discussed with the NGFF community.
This repository addresses the need for communicating the storage specification to other developers in a complete and robust way.

## What this repository contains
This directory contains notebooks that operate on lightweight datasets.
- Each notebook covers a particular aspect of the storage specification and all the edge cases of the specification are covered in at least one of the notebooks.
- All the notebooks are run every 24h. Each notebook creates a dataset, writes it to disk, reloads it in memory, rewrites it to disk to check for consistency, reloads it again in memory and plots it.
- The disk storage is committed to GitHub so that the output of each daily run is associated to a commit.
- The notebooks are run daily against both the latest `release` and the latest `main` versions of the `spatialdata` library.
- The corresponding produced data is available in the current directory, in different commits. Specifically, `release` data is tagged and both `release` and `main` data have the commit message `autorun: storage format`).
- The data is also uploaded at these two S3 location (latest) [release](https://s3.embl.de/spatialdata/developers_resources/storage_format/release) and (latest) [main](https://s3.embl.de/spatialdata/developers_resources/storage_format/main).

## How to use this repository
Practically, a third party tool (e.g. R reader, format converter, JavaScript data visualizer, etc.) that runs correctly on the lightweight datasets from this repository, is guaranteed to run correctly on any SpatialData dataset.

We recommend the following.
- Implement your readers on the latest `release` version of the data; you can checkout it with the following command (run from the current folder):
```bash
git checkout $(git describe --tags --abbrev=0)
# TODO: test the command
```
- Set up an automated test (e.g. daily) that downloads the latest `release` (with the above command) and runs your reader on it. Optionally you can also run your tool against the latest `main` version of the data (`git checkout`)
- If your reader fails, you can check the corresponding commit in this repository to see what has changed in the storage specification and update your reader accordingly; in particular, to compare the current release with the latest release you can use the following command (run from the current folder):
```bash
git diff \
    $(git rev-list -n 1 $(git describe --tags --abbrev=0)) \
    $(git rev-list -n 1 main) -- data
# TODO: test the command
```

## Important technical notes
- The most crucial part of the metadata is stored, for each spatial element, in the `.zattr` file. Example: <transformation_identity.zarr/images/blobs_image/.zattrs>
- The `zmetadata` in the root folder stores redundant information and is used for storage systems that do not support `ls` operations (e.g. S3). Example: <transformation_identity.zarr/zmetadata>
