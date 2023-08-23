from spatialdata._io._utils import _are_directories_identical
import spatialdata as sd
import os
import zarr
from ome_zarr.io import parse_url
import tempfile
import shutil

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

    shutil.make_archive(f1, 'zip', f1)

def make_index_html(elements: list[str]) -> None:
    # Define the beginning of the HTML string
    html = """
    <html>
    <head>
    <title>Index</title>
    </head>
    <body>
    <table border="1">
    <tr>
    <th>Element</th>
    <th>Link</th>
    <th>Zip</th>
    </tr>
    """

    BASE_URL = 'https://s3.embl.de/spatialdata/developers_resources/storage_format/'
    
    # Populate the HTML string with table data
    for element in elements:
        html += f"<tr><td>{element}</td><td><a href='{BASE_URL}{element}.zarr'>{element}.zarr</a></td><td><a href='{BASE_URL}{element}.zarr.zip'>{element}.zarr.zip</a></td></tr>\n"
    
    # Close the HTML string
    html += """
    </table>
Note: opening the above .zarr URLs in a web browser would not work, you need to treat the URLs as Zarr stores. For example if you append `/.zgroup` to any of the .zarr URLs above you will be able to see that file.
    </body>
    </html>
    """
    
    # Write the HTML string to a file
    with open("index.html", "w") as file:
        file.write(html)

if __name__ == '__main__':
    notebooks = [f.replace('.ipynb', '') for f in os.listdir() if f.endswith('.ipynb') and f != '__template__.ipynb']
    make_index_html(notebooks)