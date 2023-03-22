import os
from transkribus_utils import ACDHTranskribusUtils
import requests

base_row_dump_url = "https://raw.githubusercontent.com/bundesverfassung-oesterreich/bv-entities/main/json_dumps/document.json"
GOOBI_BASE_URL = "https://viewer.acdh.oeaw.ac.at/viewer/sourcefile?id="
FILE_ID = os.environ.get('FILE_ID', 'kelsen-entwurf-2')
COL_ID = int(os.environ.get('COL_ID', "188933"))

def load_metadata_from_dump(dump_url):
    get_req = requests.get(dump_url)
    json_data = get_req.json()
    meta_data_objs_by_transkribus_id = {}
    for doc_row in json_data.values():
        mets_dict = doc_row
        transcribus_col_id = mets_dict["transkribus_col_id"]
        if not transcribus_col_id:
            pass
        else:
            if transcribus_col_id not in meta_data_objs_by_transkribus_id:
                meta_data_objs_by_transkribus_id[transcribus_col_id] = {}
            meta_data_objs_by_transkribus_id[transcribus_col_id][mets_dict["transkribus_doc_id"]] = mets_dict
    return meta_data_objs_by_transkribus_id

client = ACDHTranskribusUtils()
for transkribus_collection_id, items in load_metadata_from_dump(base_row_dump_url).items():
    for transcribus_doc_id, entity in items.values():
        bv_id = entity["bv_id"]
        upload = client.upload_mets_file_from_url(
            f"{GOOBI_BASE_URL}{bv_id}",
            transkribus_collection_id)
        if upload:
            print("upload worked, all good")
