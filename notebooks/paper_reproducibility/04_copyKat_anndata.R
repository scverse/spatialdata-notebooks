

library('optparse')
library('anndata')
library('data.table')
library('tidyverse')
library('RColorBrewer')
library('circlize')
library('magrittr')
library('igraph')
library('limma')
library('resample')
library('scran')
library('stringr')
library('dendextend')
library('Seurat')
library('copykat')

option_list = list(
  make_option(c("-i", "--input"), type="character", default=NULL,
              help="dataset file name", metavar="character"),
  make_option(c("--data_dir"), type="character", default='.',
              help="input data directory", metavar="character"),
  make_option(c("--out_dir"), type="character", default='.',
              help="output directory", metavar="character"),
  make_option(c("--n_hvg"), type="numeric", default=NA,
              help="number of highly variable genes", metavar="numeric"),
  make_option(c("--tag"), type="character", default='tag',
              help="name of the project", metavar="character"),
  make_option(c("--n_cores"), type="numeric", default=1,
              help="number of cores", metavar="numeric"),
  make_option(c("--n_clones"), type="numeric", default=3,
              help="number of cores", metavar="numeric"),
  make_option(c("--cellid_col"), type="character", default=NA,
              help="number of cores", metavar="character"),
  make_option(c("--min_chr"), type="numeric", default=1,
              help="minimal number of genes per chromosome for cell filtering", metavar="numeric"),
  make_option(c("--win_size"), type="numeric", default=25,
              help="minimal window sizes for segmentation", metavar="numeric"),
  make_option(c("-o", "--out"), type="character", default="out.h5ad",
            help="output file name [default= %default]", metavar="character")
);

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);


# opt = list(data_dir= 'data_tidy', input= 'visium.h5ad', n_hvg=10000, tag='test_script', n_cores=30, n_clones=4, cellid_col='barcode', out='visium_copyKat.h5ad', min_chr=1, win_size=25)
adata_f = file.path(opt$data_dir, opt$input)
adata   = adata_f %>% read_h5ad
adata$obs$clone = 'not detected'


# adata= visium
# opt = list(tag='visium', n_hvg=300, n_cores=10, min_chr=1, win_size=10, cellid_col='barcode', n_clones=4, out='out.h5ad')

obs_dt = data.table(adata$obs)
obs_dt[, cell.names := obs_dt[[opt$cellid_col]]]
rownames(adata) = obs_dt$cell.names
obs_dt %>% setkey('cell.names')

adata_st = CreateSeuratObject(counts = t(adata$X), project = opt$tag, min.cells = 0, min.features = 0)
if(!is.na(opt$n_hvg)){
  adata_st = FindVariableFeatures(adata_st, selection.method = "vst", nfeatures = opt$n_hvg)
  adata_st = adata_st[VariableFeatures(adata_st),]
}
exp.rawdata = as.matrix(adata_st@assays$RNA@counts)
# print(dim(exp.rawdata))
# length(obs_dt[opt$cellid_col])
# colnames(exp.rawdata) = obs_dt[['cell.names']]

copykat_obj = copykat(
    rawmat=exp.rawdata,
    # id.type="S",
    ngene.chr=opt$min_chr,
    win.size=opt$win_size,
    KS.cut=0.1,
    sam.name=opt$tag,
    # distance="euclidean",
    # norm.cell.names=adata$obs$barcode,
    # output.seg="FLASE",
    plot.genes="FALSE",
    # genome="hg20",
    n.cores=opt$n_cores
  )
preds = copykat_obj$prediction %>%
  data.table %>%
  setkey('cell.names') %>%
  .[obs_dt] %>%
  setkey('cell.names') %>%
  setnames('copykat.pred', 'clone')
tumor_cells = preds[preds$clone=="aneuploid", cell.names]
tumor_mat   = copykat_obj$CNAmat
colnames(tumor_mat) = str_replace(colnames(tumor_mat), '\\.', '-')
tumor_mat   = tumor_mat[, which(colnames(tumor_mat) %in% tumor_cells)]
hcc         = hclust(parallelDist::parDist(t(tumor_mat),threads =opt$n_cores, method = "euclidean"), method = "ward.D2") %>%
  cutree(opt$n_clones)
preds[names(hcc), clone := hcc]
preds[is.na(clone) | clone == 'not.defined', clone:='not detected']
preds %<>% setnames('cell.names', opt$cellid_col)
preds %<>% .[, .SD, .SDcols = unique(names(preds))]
preds %>% setkey(barcode)
adata$obs = data.frame(preds[rownames(adata)])
write_h5ad(adata, opt$out)
