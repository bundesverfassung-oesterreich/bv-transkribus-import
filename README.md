# bv-transkribus-import
workflow repo to fetch mets files from goobi and ingest them to transkribus


## development

* clone the repo `gh repo clone bundesverfassung-oesterreich/bv-transkribus-import`
* create a virtual env `virtualenv env`
* source it `source env/bin/activate`
* update pip `pip install -U pip`
* install dependencies `pip install -r requirments.txt`
* provide Transkribus credentials in a file called `secret.env` as in `dummy.env`
* set env varibales by running `source export_env_variables.sh`