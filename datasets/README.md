# Spatial omics datasets

Here you can find all datasets necessary to run the example notebooks already converted to the ZARR file format.

If you want to convert additional datasets check out the scripts available in the [spatialdata sandbox](https://github.com/giovp/spatialdata-sandbox).

| Technology                                | Sample                                                    | File Size | Filename (spatialdata-sandbox) | download data                                                                                   | work with data remotely (**see note below**)                                               | license           |
| :---------------------------------------- | :-------------------------------------------------------- | --------: | :----------------------------- | :---------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- | :---------------- |
| Visium HD                                 | Mouse intestin [^2]                                       |      1 GB | visium_hd_3.0.0_id             | [.zarr.zip](https://s3.embl.de/spatialdata/spatialdata-sandbox/visium_hd_3.0.0_io.zip)          | [S3](https://s3.embl.de/spatialdata/spatialdata-sandbox/visium_hd_3.0.0_io.zarr/)          | CCA               |
| Visium                                    | Breast cancer [^3]                                        |    1.5 GB | visium_associated_xenium_io    | [.zarr.zip](https://s3.embl.de/spatialdata/spatialdata-sandbox/visium_associated_xenium_io.zip) | [S3](https://s3.embl.de/spatialdata/spatialdata-sandbox/visium_associated_xenium_io.zarr/) | CCA               |
| Xenium                                    | Breast cancer [^3]                                        |    2.8 GB | xenium_rep1_io                 | [.zarr.zip](https://s3.embl.de/spatialdata/spatialdata-sandbox/xenium_rep1_io.zip)              | [S3](https://s3.embl.de/spatialdata/spatialdata-sandbox/xenium_rep1_io.zarr/)              | CCA               |
| Xenium                                    | Breast cancer [^3]                                        |    3.7 GB | xenium_rep2_io                 | [.zarr.zip](https://s3.embl.de/spatialdata/spatialdata-sandbox/xenium_rep2_io.zip)              | [S3](https://s3.embl.de/spatialdata/spatialdata-sandbox/xenium_rep2_io.zarr/)              | CCA               |
| CyCIF (MCMICRO output)                    | Small lung adenocarcinoma [^4]                            |    250 MB | mcmicro_io                     | [.zarr.zip](https://s3.embl.de/spatialdata/spatialdata-sandbox/mcmicro_io.zip)                  | [S3](https://s3.embl.de/spatialdata/spatialdata-sandbox/mcmicro_io.zarr/)                  | CC BY-NC 4.0 DEED |
| MERFISH                                   | Mouse brain [^5]                                          |     50 MB | merfish                        | [.zarr.zip](https://s3.embl.de/spatialdata/spatialdata-sandbox/merfish.zip)                     | [S3](https://s3.embl.de/spatialdata/spatialdata-sandbox/merfish.zarr/)                     | CC0 1.0 DEED      |
| MIBI-TOF                                  | Colorectal carcinoma [^6]                                 |     25 MB | mibitof                        | [.zarr.zip](https://s3.embl.de/spatialdata/spatialdata-sandbox/mibitof.zip)                     | [S3](https://s3.embl.de/spatialdata/spatialdata-sandbox/mibitof.zarr/)                     | CC BY 4.0 DEED    |
| Imaging Mass Cytometry (Steinbock output) | 4 different cancers (SCCHN, BCC, NSCLC, CRC) [^7][^8][^9] |    820 MB | steinbock_io                   | [.zarr.zip](https://s3.embl.de/spatialdata/spatialdata-sandbox/steinbock_io.zip)                | [S3](https://s3.embl.de/spatialdata/spatialdata-sandbox/steinbock_io.zarr/)                | CC BY 4.0 DEED    |
| Molecular Cartography (SPArrOW output)    | Mouse Liver [^10][^11]                                    |     70 MB | MouseLiver                     | [.zarr.zip](https://s3.embl.de/spatialdata/spatialdata-sandbox/mouse_liver.zip)                 | [S3](https://s3.embl.de/spatialdata/spatialdata-sandbox/mouse_liver.zarr)                  | CC BY 4.0 DEED    |

For the first 3 datasets, we also provide a version of them in which they are all aligned in a common coordinate system, and where we added the cell-type information, as described in our paper, to annotate the Xenium cells.
| Technology | Sample | File Size | Filename (spatialdata-sandbox) | download data | work with data remotely (**see note below**) | license |
| :---------------------------------------- | :-------------------------------------------------------- | --------: | :-------------------------- | :---------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- | :---------------- |
| Visium | Breast Cancer [^3] | 1.5 GB | visium_associated_xenium_io | [.zarr.zip](https://s3.embl.de/spatialdata/spatialdata-sandbox/visium_associated_xenium_io_aligned.zip) | [S3](https://s3.embl.de/spatialdata/spatialdata-sandbox/visium_associated_xenium_io_aligned.zarr/) | CCA |
| Xenium | Breast Cancer [^3] | 2.8 GB | xenium_rep1_io | [.zarr.zip](https://s3.embl.de/spatialdata/spatialdata-sandbox/xenium_rep1_io_aligned.zip) | [S3](https://s3.embl.de/spatialdata/spatialdata-sandbox/xenium_rep1_io_aligned.zarr/) | CCA |
| Xenium | Breast Cancer [^3] | 3.7 GB | xenium_rep2_io | [.zarr.zip](https://s3.embl.de/spatialdata/spatialdata-sandbox/xenium_rep2_io_aligned.zip) | [S3](https://s3.embl.de/spatialdata/spatialdata-sandbox/xenium_rep2_io_aligned.zarr/) | CCA |

**Note on S3 storage:** opening the S3 URLs in a web browser will not work, you need to treat the URLs as Zarr stores. For example if you append `.zgroup` to any of the URLs above you will be able to see that file.

## Licenses abbreviations

- CCA: Creative Common Attribution
- CC0 1.0 DEED: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication
- CC BY 4.0 DEED: Creative Common Attribution 4.0 International
- CC BY-NC 4.0 DEED: Creative Common Attribution-NonCommercial 4.0 International

The data retains the license of the original published data.

<!-- to add: raccoon, blobs, "additional resources for methods developers" -->
<!-- Artificial datasets
| Description | File Size| Filename                     | download data                                                                                   | work with data remotely [^1]                                                               |
| :--------------------- | :------------------------- | --------:| :--------------------------  | :---------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- || -                      | -                          |     11 kB| toy                          | [.zarr.zip](https://s3.embl.de/spatialdata/spatialdata-sandbox/toy.zip)                         | [S3](https://s3.embl.de/spatialdata/spatialdata-sandbox/toy.zarr/)                         | -->

# Artificial datasets

Also, here you can find [additional datasets and resources for methods developers](https://github.com/scverse/spatialdata-notebooks/blob/main/notebooks/developers_resources/storage_format/).

# References

If you use the datasets please cite the original sources and double-check their license.

[^2]: From https://www.10xgenomics.com/datasets/visium-hd-cytassist-gene-expression-libraries-of-mouse-intestine

[^3]: Janesick, A. et al. High resolution mapping of the breast cancer tumor microenvironment using integrated single cell, spatial and in situ analysis of FFPE tissue. bioRxiv 2022.10.06.510405 (2022) doi:10.1101/2022.10.06.510405.

[^4]: Schapiro, D. et al. MCMICRO: A scalable, modular image-processing pipeline for multiplexed tissue imaging. Cold Spring Harbor Laboratory 2021.03.15.435473 (2021) doi:10.1101/2021.03.15.435473.

[^5]: Moffitt, J. R. et al. Molecular, spatial, and functional single-cell profiling of the hypothalamic preoptic region. Science 362, (2018).

[^6]: Hartmann, F. J. et al. Single-cell metabolic profiling of human cytotoxic T cells. Nat. Biotechnol. (2020) doi:10.1038/s41587-020-0651-8.

[^7]: Windhager, J., Bodenmiller, B. & Eling, N. An end-to-end workflow for multiplexed image processing and analysis. bioRxiv 2021.11.12.468357 (2021) doi:10.1101/2021.11.12.468357.

[^8]: Eling, N. & Windhager, J. Example imaging mass cytometry raw data. (2022). doi:10.5281/zenodo.5949116.

[^9]: Eling, N. & Windhager, J. steinbock results of IMC example data. (2022). doi:10.5281/zenodo.7412972.

[^10]: Guilliams, Martin, et al. "Spatial proteogenomics reveals distinct and evolutionarily conserved hepatic macrophage niches." Cell 185.2 (2022) doi:10.1016/j.cell2021.12.018

[^11]: Pollaris, Lotte, et al. "SPArrOW: a flexible, interactive and scalable pipeline for spatial transcriptomics analysis." bioRxiv (2024) doi:10.1101/2024.07.04.601829
