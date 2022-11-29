#!/bin/bash
#setup the virtual environment.
deactivate 
rm -rf ./data_engineering_venv
python3 -m venv data_engineering_venv
source ./data_engineering_venv/bin/activate
. ir.sh

#Download from google drive.


echo "****************************************************************************************"
echo "*                                                                                      *"
echo "* Downloading Data Files from Google drive                                             *"
echo "* https://drive.google.com/drive/folders/1vi2pt28G0zxV7hYINUfpktZnV7EKR8U9?usp=sharing *"
echo "*                                                                                      *"
echo "****************************************************************************************"

DIRECTORY="./datasets/"

if [ -d "$DIRECTORY" ]; then
while true; do

        echo "****************************************"
        echo "*                                      *"
        echo "* The datasets directory is present    *"
        echo "* present.                             *"
        echo "*   Press \"D\" to download the          *"
        echo "*   (overwrite the datasets).          *"
        echo "*   Press \"S\" skip downloading.        *"
        echo "*                                      *"        
        echo "****************************************"


    read -p "Do you wish to download or Skip? [D/S]:" ds
    case $ds in
        [Ss]* ) deactivate;return;;
        [Dd]* ) break;;
        * ) echo "Please answer \"d\" or \"s\".";;
    esac
done        
fi


gdown https://drive.google.com/drive/folders/1vi2pt28G0zxV7hYINUfpktZnV7EKR8U9?usp=sharing -O ./datasets --folder 

deactivate