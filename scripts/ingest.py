import os
from transkribus_utils import ACDHTranskribusUtils


GOOBI_BASE_URL = "https://viewer.acdh.oeaw.ac.at/viewer/sourcefile?id="
FILE_ID = os.environ.get('FILE_ID', 'kelsen-entwurf-2')
METS_URL = f"{GOOBI_BASE_URL}{FILE_ID}"
COL_ID = int(os.environ.get('COL_ID', "188933"))

client = ACDHTranskribusUtils()
upload = client.upload_mets_file_from_url(METS_URL, COL_ID)
if upload:
    print("upload worked, all good")
