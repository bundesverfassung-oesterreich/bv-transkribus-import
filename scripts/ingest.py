from transkribus_utils.transkribus_utils import (
    ACDHTranskribusUtils,
    get_title_from_mets,
)
import requests

base_row_dump_url = "https://raw.githubusercontent.com/bundesverfassung-oesterreich/bv-entities/main/json_dumps/document.json"
GOOBI_BASE_URL = "https://viewer.acdh.oeaw.ac.at/viewer/sourcefile?id="


def load_metadata_from_dump(dump_url):
    # # loading doc metadata (baserow ump) from url
    get_req = requests.get(dump_url)
    json_data = get_req.json()
    meta_data_objs_by_transkribus_id = {}
    for metadata_dict in json_data.values():
        transcribus_col_id = metadata_dict["transkribus_col_id"]
        transkribus_doc_id = metadata_dict["transkribus_doc_id"]
        if bool(transcribus_col_id) and not bool(transkribus_doc_id):
            # # entrys without collection id are being ignored
            # # and only entrys without doc id get processed
            # # regardless if field is empty string or None
            if transcribus_col_id not in meta_data_objs_by_transkribus_id:
                meta_data_objs_by_transkribus_id[transcribus_col_id] = {}
            meta_data_objs_by_transkribus_id[transcribus_col_id][
                metadata_dict["bv_id"]
            ] = metadata_dict["doc_title"]
    return meta_data_objs_by_transkribus_id


def upload_goobidata_via_mets():
    client = ACDHTranskribusUtils()
    # # get metadata from base-row dump:
    # # {collection_id: {
    # #         bv_id:doc_title,
    # #     }
    # # }
    metadata = load_metadata_from_dump(base_row_dump_url)
    for transkribus_collection_id, items in metadata.items():
        for bv_id, doc_title in items.items():
            mets_url = f"{GOOBI_BASE_URL}{bv_id}"
            # # check if doc_title allready exists in collection
            doc_title = get_title_from_mets(mets_url)
            document_from_title = client.search_for_document(
                title=doc_title, col_id=transkribus_collection_id
            )
            if document_from_title:
                # maybe write this to baserow
                print(
                    f"Document with title '{doc_title}' already exists in collection '{transkribus_collection_id}'. Upload canceled."
                )
            else:
                # # upload mets to transkribus
                print(f"uplaoding '{doc_title}' to '{transkribus_collection_id}'")
                upload = client.upload_mets_file_from_url(
                    mets_url,
                    transkribus_collection_id,
                    better_images=True,
                )
                if upload:
                    print("upload worked, all good")
                else:
                    print(
                        f"upload of '{doc_title}' to '{transkribus_collection_id}' failed."
                    )
    if len(metadata) == 0:
        print("Nothing to be done!")


if __name__ == "__main__":
    upload_goobidata_via_mets()
