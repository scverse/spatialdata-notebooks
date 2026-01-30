# Spatial omics datasets

Here you can find all datasets necessary to run the example notebooks already converted
to the SpatialData Zarr file format.

Scripts to convert data from several other technologies into SpatialData Zarr are
available in the [spatialdata sandbox](https://github.com/giovp/spatialdata-sandbox); in
particular:

- CyCIF (MCMICRO output)[^4]
- Imaging Mass Cytometry, IMC (Steinbock output)[^7][^8][^9]
- seqFISH

| Technology                             | Sample                      | File Size | Filename (spatialdata-sandbox) | license   |
|:---------------------------------------|:----------------------------|----------:|:-------------------------------|:----------|
| Visium HD                              | Mouse intestin [^1]         |   ~2.4 GB | visium_hd_3.0.0_io             | CC BY 4.0 |
| Visium HD                              | Mouse brain [^13]           |    <200MB | visium_hd_4.0.1_io             | CC BY 4.0 |
| Visium                                 | Breast cancer [^2]          |   ~1.5 GB | visium_associated_xenium_io    | CC BY 4.0 |
| Visium                                 | Mouse brain [^14]           |    <100MB | visium                         | CC BY 4.0 |
| Xenium                                 | Breast cancer [^2]          |   ~2.8 GB | xenium_rep1_io                 | CC BY 4.0 |
| Xenium                                 | Lung cancer [^3]            |   ~5.4 GB | xenium_2.0.0_io                | CC BY 4.0 |
| MERFISH                                | Mouse brain [^5]            |    ~50 MB | merfish                        | CC0 1.0   |
| MIBI-TOF                               | Colorectal carcinoma [^6]   |    ~25 MB | mibitof                        | CC BY 4.0 |
| Molecular Cartography (SPArrOW output) | Mouse Liver [^10][^11]      |    ~70 MB | mouse_liver                    | CC BY 4.0 |
| SpaceM                                 | Hepa and NIH3T3 cells [^12] |    ~60 MB | spacem_hepanih3t3              | CC BY 4.0 |

*Please select the dataset and version below to download the data.

```{raw} html
<div style="margin: 1em 0 2em 0; padding: 1em; border: 1px solid #444; border-radius: 6px; max-width: 600px;">
  <label for="dataset-select"><strong>Dataset:</strong></label>
  <select id="dataset-select" style="margin: 0.3em 0 0.8em 0.5em; padding: 0.3em;">
    <option value="visium_hd_3.0.0_io">visium_hd_3.0.0_io</option>
    <option value="visium_hd_4.0.1_io">visium_hd_4.0.1_io</option>
    <option value="visium_associated_xenium_io">visium_associated_xenium_io</option>
    <option value="visium">visium</option>
    <option value="xenium_rep1_io">xenium_rep1_io</option>
    <option value="xenium_2.0.0_io">xenium_2.0.0_io</option>
    <option value="merfish">merfish</option>
    <option value="mibitof">mibitof</option>
    <option value="mouse_liver">mouse_liver</option>
    <option value="spacem_hepanih3t3">spacem_hepanih3t3</option>
  </select>
  <br>
  <label for="version-select"><strong>Version:</strong></label>
  <select id="version-select" style="margin: 0.3em 0 0.8em 0.5em; padding: 0.3em;">
    <option value="_spatialdata_0.7.0_spatialdata_io_0.6.0">spatialdata 0.7.0 / spatialdata-io 0.6.0</option>
  </select>
  <br>
  <strong>Download link: </strong>
  <a id="download-link" href="https://s3.embl.de/spatialdata/spatialdata-sandbox/visium_hd_3.0.0_io_spatialdata_0.7.0_spatialdata_io_0.6.0.zip">
    https://s3.embl.de/spatialdata/spatialdata-sandbox/visium_hd_3.0.0_io_spatialdata_0.7.0_spatialdata_io_0.6.0.zip
  </a>
  <script>
    function updateDownloadLink() {
      var dataset = document.getElementById('dataset-select').value;
      var version = document.getElementById('version-select').value;
      var url = 'https://s3.embl.de/spatialdata/spatialdata-sandbox/' + dataset + version + '.zip';
      var link = document.getElementById('download-link');
      link.href = url;
      link.textContent = url;
    }
    document.getElementById('dataset-select').addEventListener('change', updateDownloadLink);
    document.getElementById('version-select').addEventListener('change', updateDownloadLink);
  </script>
</div>
```

## Licenses abbreviations

- CC0 1.0: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication
- CC BY 4.0: Creative Common Attribution 4.0 International
- CC BY-NC 4.0: Creative Common Attribution-NonCommercial 4.0 International

The data retains the license of the original published data.

# Artificial datasets

Also, here you can find [additional datasets and resources for methods developers](https://github.com/scverse/spatialdata-notebooks/blob/main/notebooks/developers_resources/storage_format/).

# References

If you use the datasets please cite the original sources and double-check their license.

[^1]: From https://www.10xgenomics.com/datasets/visium-hd-cytassist-gene-expression-libraries-of-mouse-intestine

[^2]: Janesick, A. et al. High resolution mapping of the breast cancer tumor
microenvironment using integrated single cell, spatial and in situ analysis of FFPE
tissue. bioRxiv 2022.10.06.510405 (2022) doi:
10.1101/2022.10.06.510405. https://www.10xgenomics.com/products/xenium-in-situ/preview-dataset-human-breast

[^3]: From https://www.10xgenomics.com/datasets/preview-data-ffpe-human-lung-cancer-with-xenium-multimodal-cell-segmentation-1-standard

[^4]: Schapiro, D. et al. MCMICRO: A scalable, modular image-processing pipeline for
multiplexed tissue imaging. Cold Spring Harbor Laboratory 2021.03.15.435473 (2021) doi:
10.1101/2021.03.15.435473.

[^5]: Moffitt, J. R. et al. Molecular, spatial, and functional single-cell profiling of
the hypothalamic preoptic region. Science 362, (2018).

[^6]: Hartmann, F. J. et al. Single-cell metabolic profiling of human cytotoxic T cells.
Nat. Biotechnol. (2020) doi:10.1038/s41587-020-0651-8.

[^7]: Windhager, J., Bodenmiller, B. & Eling, N. An end-to-end workflow for multiplexed
image processing and analysis. bioRxiv 2021.11.12.468357 (2021) doi:
10.1101/2021.11.12.468357.

[^8]: Eling, N. & Windhager, J. Example imaging mass cytometry raw data. (2022). doi:
10.5281/zenodo.5949116.

[^9]: Eling, N. & Windhager, J. steinbock results of IMC example data. (2022). doi:
10.5281/zenodo.7412972.

[^10]: Guilliams, Martin, et al. "Spatial proteogenomics reveals distinct and
evolutionarily conserved hepatic macrophage niches." Cell 185.2 (2022) doi:
10.1016/j.cell2021.12.018

[^11]: Pollaris, Lotte, et al. "SPArrOW: a flexible, interactive and scalable pipeline
for spatial transcriptomics analysis." bioRxiv (2024) doi:10.1101/2024.07.04.601829

[^12]: See https://github.com/giovp/spatialdata-sandbox/blob/main/spacem_helanih3t3/README.md

[^13]: From https://www.10xgenomics.com/datasets/visium-hd-three-prime-mouse-brain-fresh-frozen

[^14]: Available here: https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-11114. Linked publications: https://www.nature.com/articles/s43587-022-00246-4, https://www.nature.com/articles/s41587-021-01139-4

# Opening an issue

If you notice any issues, such as a changed dataset, a removed dataset, or missing
dataset information, please open a GitHub issue so we can address it. Thank you!
