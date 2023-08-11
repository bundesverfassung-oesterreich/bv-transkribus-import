from transkribus_utils.transkribus_utils import ACDHTranskribusUtils
import requests
import ingest

client = ACDHTranskribusUtils()
processed_docs_by_collection = ingest.load_metadata_from_dump(ingest.base_row_dump_url)


class Job:
    def __init__(self, job_json: dict):
        self.job_id = job_json["jobId"]
        self.doc_id = job_json["docId"]
        self.collection_id = job_json["colId"]
        self.doc_title = job_json["docTitle"]
        self.status = job_json["state"]
        self.done = bool(self.status == "FINISHED")
        self.bv_doc_id = ""


def get_jobs(filter_dict: dict):
    jobs_request_result = requests.get("https://transkribus.eu/TrpServer/rest/jobs/list", client.login_cookie)
    jobs_request_result_json = jobs_request_result.json()
    jobs = []
    for jjob in jobs_request_result_json:
        remove = False
        for field, value in filter_dict.items():
            if jjob[field] != value:
                remove = True
                break
        if not remove:
            jobs.append(
                Job(jjob)
            )
    return jobs


creation_jobs = get_jobs(
    {
        "type" : "Create Document"
    }
)

for job in creation_jobs:
    job: Job
    if job.done:
        if job.collection_id in processed_docs_by_collection:
            potential_docs = processed_docs_by_collection[job.collection_id]
            for bv_doc_id, doc_title in potential_docs:
                if doc_title.strip() == job.doc_title.strip():
                    job.bv_doc_id = bv_doc_id
                    print(job.doc_title)