# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "extensions"))


# -- Project information -----------------------------------------------------

# info = metadata("spatialdata-notebooks")
# project = info["Name"]
# author = info["Author"]
# copyright = f"{datetime.now():%Y}, {author}."
# version = info["Version"]

# # The full version, including alpha/beta/rc tags
# release = info["Version"]
project_name = "spatialdata-notebooks"
repository_url = f"https://github.com/scverse/{project_name}"

bibtex_bibfiles = ["references.bib"]
templates_path = ["_templates"]
nitpicky = True  # Warn about broken links
needs_sphinx = "4.0"

html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": "scverse",  # Username
    "github_repo": project_name,  # Repo name
    "github_version": "main",  # Version
    "conf_py_path": "/docs/",  # Path in the checkout to the docs root
}

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings.
# They can be extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "myst_nb",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinxcontrib.bibtex",
    "sphinx_autodoc_typehints",
    "sphinx.ext.mathjax",
    "IPython.sphinxext.ipython_console_highlighting",
    "sphinx_design",
    *[p.stem for p in (HERE / "extensions").glob("*.py")],
]

autosummary_generate = True
autodoc_member_order = "groupwise"
default_role = "literal"
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_use_rtype = True  # having a separate entry generally helps readability
napoleon_use_param = True
myst_heading_anchors = 3  # create anchors for h1-h3
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
    "html_admonition",
]
myst_url_schemes = ("http", "https", "mailto")
nb_output_stderr = "remove"
nb_execution_mode = "off"
nb_merge_streams = True
typehints_defaults = "braces"

source_suffix = {
    ".rst": "restructuredtext",
    ".ipynb": "myst-nb",
    ".myst": "myst-nb",
}

intersphinx_mapping = {
    "anndata": ("https://anndata.readthedocs.io/en/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "geopandas": ("https://geopandas.org/en/stable/", None),
    "xarray": ("https://docs.xarray.dev/en/stable/", None),
    "datatree": ("https://datatree.readthedocs.io/en/latest/", None),
}


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# note: these patterns should also be added in spatialdata/docs/conf.py
exclude_patterns = [
    "_build",
    "Thumbs.db",
    "**.ipynb_checkpoints",
    "data",
    "temp",
    "notebooks/paper_reproducibility",
    "notebooks/examples/*.zarr",
    "Readme.md",  # hack cause git his acting up
    "notebooks/developers_resources/storage_format/*.ipynb",
    "notebooks/developers_resources/storage_format/Readme.md",
    "notebooks/examples/technology_stereoseq.ipynb",  # no public data available
    "notebooks/examples/technology_curio.ipynb",  # no public data available
    "notebooks/examples/technology_cosmx.ipynb",  # temporarily removed until the new reader and datasets are available
    "notebooks/examples/stereoseq_data/*",
]
# Ignore warnings.
nitpicky = False  # TODO: solve upstream.
nitpick_ignore = [
    # these two files are not available when building the docs from
    # spatialdata-notebook (but they are when building the docs from spatialdata)
    ("myst", "../../../../api.md"),
    ("myst", "../../../../glossary.md"),
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_title = project_name

html_theme_options = {
    "repository_url": repository_url,
    "use_repository_button": True,
    "navigation_with_keys": True,
}

pygments_style = "default"


def setup(app):
    """App setup hook."""
    app.add_config_value(
        "recommonmark_config",
        {
            "auto_toc_tree_section": "Contents",
            "enable_auto_toc_tree": True,
            "enable_math": True,
            "enable_inline_math": False,
            "enable_eval_rst": True,
        },
        True,
    )
