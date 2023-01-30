##
import hashlib
import os
import zipfile

# please manually download the data from https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com
# /svw96g68dv-1.zip
CHECKSUM = "eebd948d752a6d16b9c972e3fc4b293c4fa0fc16edbcbec41c8c5d48acf2143b"

##
path = os.path.join("./data/lundeberg/", "svw96g68dv-1.zip")
if hashlib.sha256(open(path, "rb").read()).hexdigest() != CHECKSUM:
    print("checksum mismatch")
else:
    print("checksum ok")

##
# unzip the data
unzipped_path = path.replace(".zip", "")
if not os.path.exists(unzipped_path):
    print("Unzipping the data")
    with zipfile.ZipFile(path) as zip_ref:
        zip_ref.extractall(os.path.dirname(unzipped_path))
    print("data unzipped")
assert os.path.isdir(unzipped_path)
