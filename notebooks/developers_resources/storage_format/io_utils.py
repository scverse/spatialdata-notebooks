from spatialdata._io._utils import _are_directories_identical
import spatialdata as sd
import os
import zarr
from ome_zarr.io import parse_url
import tempfile

def delete_old_data(name: str) -> None:
    f1 = f'{name}.zarr'
    if os.path.isdir(f1):
        store = parse_url(f1, mode="w").store
        root = zarr.group(store=store, overwrite=True)
        store.close()
        os.remove(os.path.join(f1, '.zgroup'))
        os.rmdir(f1)
    """
    Safely delete an old Zarr store, it if exists.

    name : str
        The name of the file (without extension) to write to and read from.
    """
    
def write_sdata_and_check_consistency(sdata: sd.SpatialData, name: str) -> None:
    """
    Write SpatialData instance to file, reload it, and check for consistency.

    This function writes the input `sdata` to a file using the specified `name`.zarr.
    The data is then reloaded from the file and written again, and the two outputs 
    folders are compared recursively and binary wise, to check for the consistency
    of the read-write operations.

    Parameters
    ----------
    sdata : sd.SpatialData
        The SpatialData instance to be written to a file.
    name : str
        The name of the file to write to and read from.

    Returns
    -------
    None

    Examples
    --------
    >>> sdata = sd.SpatialData() # assume SpatialData instance is created
    >>> write_sdata_and_check_consistency(sdata, 'testfile') # will create testfile.zarr
    """

    f1 = f'{name}.zarr'
    assert not os.path.exists(f1)
    sdata.write(f1)
        
    with tempfile.TemporaryDirectory() as tmpdir:
        sdata2 = sd.read_zarr(f1)
        f2 = os.path.join(tmpdir, f'{name}2.zarr')
        sdata2.write(f2)
        assert _are_directories_identical(f1, f2)