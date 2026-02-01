"""Sphinx extension: fetch the S3 bucket listing at build time and write ``_static/datasets_data.js``.

The JS file sets ``window.SPATIALDATA_DATASETS`` – a mapping of each known
dataset ID to a sorted list of version suffixes found on S3, e.g.::

    {
        "merfish": ["", "_spatialdata_0.7.0_spatialdata_io_0.6.0"],
        ...
    }

The file is registered via ``app.add_js_file()`` so that Sphinx resolves
the ``<script>`` path correctly even when the notebooks are embedded inside
a parent Sphinx project.

This avoids any browser-side CORS issues because the S3 fetch happens
server-side during the Sphinx build.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from urllib.request import urlopen
from xml.etree import ElementTree

logger = logging.getLogger(__name__)

# A suffix (the part after the dataset ID) is accepted only if it is empty
# or matches one of these patterns.  This avoids treating unrelated files
# (e.g. ``visium_io.zip``, ``visium_test.zip``) as versions of ``visium``.
_VALID_SUFFIX_RE = re.compile(r"^(_spatialdata_.+|_dev|v\d.*)$")

# Every dataset ID and suffix written into the JS file must match this
# pattern.  This is a safety check to prevent injection via unexpected S3
# key contents – only alphanumerics, dots, underscores, hyphens and plus
# signs are allowed.
_SAFE_TOKEN_RE = re.compile(r"^[A-Za-z0-9._+\-]*$")

S3_LIST_URL = "https://s3.embl.de/spatialdata/?list-type=2&prefix=spatialdata-sandbox/&delimiter=/"

# Known dataset IDs – sorted longest-first so that the greedy prefix
# matching picks the most specific ID (e.g. ``visium_hd_3.0.0_io``
# before ``visium``).
DATASET_IDS = sorted(
    [
        "visium_hd_3.0.0_io",
        "visium_hd_4.0.1_io",
        "visium_associated_xenium_io",
        "visium",
        "xenium_rep1_io",
        "xenium_2.0.0_io",
        "merfish",
        "mibitof",
        "mouse_liver",
        "spacem_helanih3t3",
    ],
    key=len,
    reverse=True,
)


def _fetch_and_write(app):
    """Fetch the S3 listing and write ``datasets_data.js`` into ``_static/``."""
    static_dir = Path(app.srcdir) / "_static"
    static_dir.mkdir(exist_ok=True)

    logger.info("[fetch_s3_datasets] Fetching %s", S3_LIST_URL)
    try:
        with urlopen(S3_LIST_URL, timeout=30) as resp:
            xml_bytes = resp.read()
    except Exception:
        logger.warning("[fetch_s3_datasets] Could not reach S3 – datasets_data.js will not be updated.")
        return

    root = ElementTree.fromstring(xml_bytes)
    ns = root.tag.split("}")[0] + "}" if "}" in root.tag else ""

    zip_files: list[str] = []
    for key_el in root.iter(f"{ns}Key"):
        key = key_el.text or ""
        if key.endswith(".zip"):
            zip_files.append(key.removeprefix("spatialdata-sandbox/"))

    # Build map: dataset_id -> sorted list of suffixes
    result: dict[str, list[str]] = {did: [] for did in DATASET_IDS}
    for filename in zip_files:
        base = filename.removesuffix(".zip")
        for did in DATASET_IDS:
            if base == did:
                result[did].append("")
                break
            suffix = base[len(did) :]
            if base.startswith(did) and _VALID_SUFFIX_RE.match(suffix):
                result[did].append(suffix)
                break

    for did in result:
        result[did].sort()

    # Safety: validate every token before embedding in a JS literal.
    for did, suffixes in result.items():
        if not _SAFE_TOKEN_RE.match(did):
            logger.warning("[fetch_s3_datasets] Skipping unsafe dataset id: %r", did)
            result[did] = []
            continue
        result[did] = [s for s in suffixes if _SAFE_TOKEN_RE.match(s)]

    js_path = static_dir / "datasets_data.js"
    json_str = json.dumps(result, indent=2)
    js_path.write_text(f"window.SPATIALDATA_DATASETS = {json_str};\n")
    logger.info("[fetch_s3_datasets] Wrote %s (%d datasets)", js_path, len(result))


def setup(app):
    app.connect("builder-inited", _fetch_and_write)
    app.add_js_file("datasets_data.js")
    return {"version": "0.2", "parallel_read_safe": True, "parallel_write_safe": True}
