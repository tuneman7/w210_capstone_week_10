#!/bin/bash
#setup the virtual environment.
deactivate 
rm -rf ./data_engineering_venv
python3 -m venv data_engineering_venv
source ./data_engineering_venv/bin/activate

pip install bs4
pip install requests

python3 download_data_new.py

deactivate
rm -rf ./data_engineering_venv



