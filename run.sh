#!/bin/bash
#get out of a viritual environment if we are in one
deactivate
. check_deps.sh > output.txt


clear

echo "*************************************"
echo "* U.C. Berkeley MIDS W210           *"
echo "* Fall 2022                         *"
echo "* Instructor(s): Cornelia & Alberto *"
echo "* Team: Ben, Ben, Blake, & Don      *"
echo "* Environment Script                *"
echo "*************************************"

echo "**********************************"
echo "* CHECKING ALL DEPENDENCIES      *"
echo "* Python Virtual Environments    *"
echo "* Poetry, Docker, K6, & Minikube *"
echo "**********************************"


echo " All Depdendencies $all_dependencies"

  if [ "$all_dependencies" -ne 1 ]; then

        echo "**********************************"
        echo "* Not all depdencies were met    *"
        echo "* Please install dependencies    *"
        echo "* and try again.                 *"
        echo "**********************************"

        if [ "$k6_present" -ne 0 ]; then
            echo "K6 is not installed."
            echo "visit https://k6.io/docs/getting-started/installation/"
            echo "**********************************"
            export all_dependencies=0
        fi

        if [ "$python_venv" -ne 0 ]; then
            echo "Python Virtual Environments are not installed."
            export all_dependencies=0
        fi

        if [ "$docker_present" -ne 0 ]; then
            echo "Docker is not installed."
            echo "**********************************"
            export all_dependencies=0
        fi  

        if [ "$minikube_present" -ne 0 ]; then
            echo "Minikube is not installed."
            echo "visit https://minikube.sigs.k8s.io/docs/start/"
            echo "**********************************"
            export all_dependencies=0
        fi  

        if [ "$poetry_present" -ne 0 ]; then
            echo "Poetry is not installed."
            echo "visit https://python-poetry.org/docs/"
            echo "**********************************"
            export all_dependencies=0
        fi  

        # if [ "$bozo_present" -ne 0 ]; then
        #     echo "Bozo not installed."
        #     export all_dependencies=0
        # fi 
        echo "**********************************"
        echo "**********************************"
        return
  fi

echo "***********************************"
echo "*                                 *"
echo "* Installing Data Engineering Env *"
echo "*   virtual environment           *"
echo "*                                 *"
echo "***********************************"

data_eng_venv_activated=0

if [ $data_eng_venv_activated == 0 ]; then
    cd data_engineering
    . setup_venv_download_files.sh
    cd ./../
fi


echo "*************************************"
echo "* Completed data engineering dl     *"
echo "* now activating website            *"
echo "*************************************"

cd web_application
. run_site.sh
cd ./../
