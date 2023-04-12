# Obtaining the datasets

The example notebooks operate on a set of spatial omics datasets that can be downloaded and converted to Zarr (OME-NGFF) with the scripts available in https://github.com/giovp/spatialdata-sandbox.

Here you can find the dataset hosted in S3 object storage.

|           Dataset           |                                          S3                                          |
| :-------------------------: | :----------------------------------------------------------------------------------: |
|          cosmx_io           |          https://s3.embl.de/spatialdata/spatialdata-sandbox/cosmx_io.zarr/           |
|         mcmicro_io          |         https://s3.embl.de/spatialdata/spatialdata-sandbox/mcmicro_io.zarr/          |
|           merfish           |           https://s3.embl.de/spatialdata/spatialdata-sandbox/merfish.zarr/           |
|           mibitof           |           https://s3.embl.de/spatialdata/spatialdata-sandbox/mibitof.zarr/           |
|        steinbock_io         |        https://s3.embl.de/spatialdata/spatialdata-sandbox/steinbock_io.zarr/         |
|             toy             |             https://s3.embl.de/spatialdata/spatialdata-sandbox/toy.zarr/             |
|           visium            |           https://s3.embl.de/spatialdata/spatialdata-sandbox/visium.zarr/            |
|          visium_io          |          https://s3.embl.de/spatialdata/spatialdata-sandbox/visium_io.zarr/          |
| visium_associated_xenium_io | https://s3.embl.de/spatialdata/spatialdata-sandbox/visium_associated_xenium_io.zarr/ |
|       xenium_rep1_io        |       https://s3.embl.de/spatialdata/spatialdata-sandbox/xenium_rep1_io.zarr/        |
|       xenium_rep2_io        |       https://s3.embl.de/spatialdata/spatialdata-sandbox/xenium_rep2_io.zarr/        |

Note: opening the above URLs in a web browser would not work, you need to treat the URLs as Zarr stores. For example if you append `.zgroup` to any of the URLs above you will be able to see that file.
