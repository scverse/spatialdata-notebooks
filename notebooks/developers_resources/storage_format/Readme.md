# Examples covering the whole storage specification

This directory offers comprehensive resources for developers that want to interface their methods with the SpatialData format in a robust way.

## Why this repository
The file storage format adopted by SpatialData is built on top of the latest version of the well-documented [OME-NGFF specification](https://ngff.openmicroscopy.org/latest/index.html), but it also uses *some* less-documented features of the OME-NGFF specification that are still [under review](https://github.com/ome/ngff/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc), or experimental storage strategies that will be eventually discussed with the NGFF community.
This repository addresses the need for communicating the storage specification to other developers in a complete and robust way.

## What this repository contains
This directory contains notebooks that operate on lightweight datasets.
- Each notebook covers a particular aspect of the storage specification and ~~all the~~ *the main (work in progress)* edge cases of the specification are covered in at least one of the notebooks.
- All the notebooks are run every 24h against the `main` branch of the `spatialdata` repository. Each notebook creates a dataset, writes it to disk, reloads it in memory, rewrites it to disk to check for consistency, reloads it again in memory and plots it.
- The disk storage is committed to GitHub so that the output of each daily run is associated to a commit, the commit message is "autorun: storage format; spatialdata from <commit hash> <optional (commit tag)>". Examples of commit messages are:
  - `autorun: storage format; spatialdata from al29fak`
  - `autorun: storage format; spatialdata from fa096da (v0.0.12)`
- The `.zarr` data produced by every run is available in the current directory, in the commit corresponding to the run.
- The data is also [uploaded to S3](https://refined-github-html-preview.kidonng.workers.dev/scverse/spatialdata-notebooks/raw/dev_notebooks/notebooks/developers_resources/storage_format/index.html), both as Zarr directories and as zipped files.

## How to use this repository
Practically, a third party tool (e.g. R reader, format converter, JavaScript data visualizer, etc.) that runs correctly on the lightweight datasets from this repository, should be guaranteed to run correctly on any SpatialData dataset.

We recommend the following.
- Implement your readers on the data from the latest run available (look for the latest commit with message `autorun: storage format; ...`).
- Set up an automated test (e.g. daily) that gets the latest converted data (you can use a `git pull` or download the data from S3) and runs your code on it.
- If your reader fails, you can inspect the corresponding commit in this repository to see what has changed in the storage specification; in particular, you may find useful to compare different commits using the GitHub compare function, accessible with the following syntax: https://github.com/scverse/spatialdata-notebooks/compare/267adb1..5847084

## Important technical notes
- The most crucial part of the metadata is stored, for each spatial element, in the `.zattr` file. [Example](transformation_identity.zarr/images/blobs_image/.zattrs).
- The `zmetadata` in the root folder stores redundant information and is used for storage systems that do not support `ls` operations (e.g. S3). [Example](transformation_identity.zarr/zmetadata).
- Please keep in mind that the data that we generate daily are produced against the latest `main` and not the latest release. This means that in the event of a format change (which should anyway happen less and less frequently as the frameworks become more mature), this does not immediately translate into a bug for the user. In fact, the user will still be using the latest release version for a while, giving time to developers to update the tools before the users are affected.
- When the format will become more mature we will provide converters between previous version of the format. Luckily, heavy data like images and labels are stable from NGFF v0.4, therefore the converters will mostly perform lightweight conversions of the metadata.
