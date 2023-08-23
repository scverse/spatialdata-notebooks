# Examples covering the whole storage specification

This repository offers comprehensive resources for developers that want to interface their methods with the SpatialData format in a robust way.

## Why this repository
The file storage format adopted by SpatialData is built on top of the latest version of the well-documented [OME-NGFF specification](https://ngff.openmicroscopy.org/latest/index.html), but it also uses some less-documented features of the OME-NGFF specification that are still under review, or experimental storage strategies that will be eventually discussed with the NGFF community.
This repository addresses the need for communicating the storage specification to other developers in a complete and robust way.

## What this repository contains
In particular:
- this directory contains notebooks that operate on small datasets which are created, written to disk, reloaded, rewritten to disk and checked for consitency, reloaded again, plotted, and finally the disk storage is uploaded to S3 (available here); # TODO add link
- each notebook covers a particular aspect of the storage specification and all the edge cases of the specification are covered in at least one of the notebooks;
- the notebooks are tested daily against the latest `release` and the latest `main` versions of the `spatialdata` library, and detected differences are reported here; # TODO add link
- also, detected differences between the previous release version are reported here. # TODO add link

## How to use this repository
Practically, a third party tool (e.g. R reader, format converter, JavaScript data visualizer, etc.) that runs correctly on the lightweight datasets from this repository, is then guaranteed to run correctly on any SpatialData dataset.
