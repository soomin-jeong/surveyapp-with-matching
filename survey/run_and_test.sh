#!/bin/bash

## Author: Ananta Lamichhane, Soo Min Jeong

########################## INTRODUCTION AND PURPOSE #############################
## This script performs all the steps to install and run both
## frontend and API server. It performs the following step:
## 1.creates a python virtual environment in survey directory
## 2. activates the venv created in 1.
## 3. Installs all necessary packages specified by backend/src/requirements.txt
## 4. Runs the flask API server using gunicorn on port 5000.
## 5. Checks if the API server is on.
## 6a. If API server can' start, breaks the process.
## 6b. If API server has started, installs necessary npm modules in survey/frontend.
## 7. After installing modules, starts the app on port 3000 in background.
## 8. Waits 5 sec. to allow app to initialize, and checks if it's on.
## 9. Ends script after coming back to the survey directory.

###################################   USAGE  ############################
## change permissions to be able to run the script: chmod +x run_and_test.sh
## run using: source run_and_test.sh


API_URL="http://localhost:5000"
SURVEY_URL="http://localhost:3000/survey"

## copy files from examples to appropriate places
echo "------------------------------------------------------------"
echo "1. Copying files from examples to appropriated directories"
cp -r $PWD/backend/examples/datasets $PWD/backend/data
cp -r $PWD/backend/examples/recommendation_lists $PWD/backend/data
cp -r $PWD/backend/examples/mailing_lists $PWD/backend/data

echo "------------------------------------------------------------"
echo "Finished copying files"
echo "------------------------------------------------------------"


echo "creating venv"

python3 -m venv venv

echo "------------------------------------------------------------"
echo "Created venv"
echo "------------------------------------------------------------"

echo "activating venv"
path=$PWD
subpath="/venv/bin/activate"
new_path="$path$subpath" #/home/ubuntu/data
source $new_path
echo "------------------------------------------------------------"
echo "activated venv"

echo "------------------------------------------------------------"
echo "install requirements"
pip install -r $PWD/backend/src/requirements.txt
echo "------------------------------------------------------------"
echo "Finished installing requirements"

echo "------------------------------------------------------------"
echo "Running backend on port 5000."
gunicorn --bind 0.0.0.0:5000 backend.src.app:app --daemon
sleep 5
echo "checking if the server is up"
HTTP_CODE=$(curl --write-out "%{http_code}\n" "$API_URL" --output output.txt --silent)

if [ $HTTP_CODE -ne 200 ]
then
    echo "1: API server is not online. Please check. The HTTP_CODE is $HTTP_CODE"
else
    echo "1: API Server is online."

    cd frontend
    echo "------------------------------------------------------------"
    echo "installing npm modules."
    npm install
    echo "------------------------------------------------------------"
    echo "Done installing npm modules."
    echo "------------------------------------------------------------"
    echo "Starging web application on port 3000"
    npm start&
    echo "------------------------------------------------------------"
    echo "Stared web app"
    echo "------------------------------------------------------------"
    echo "Waiting for web app to initialize"
    sleep 5
    echo "------------------------------------------------------------"
    echo "checking if the server is up"
    HTTP_CODE=$(curl --write-out "%{http_code}\n" "$SURVEY_URL" --output output.txt --silent)

    if [$HTTP_CODE -ne 200]
    then
      echo "2: Survey server is not online. Please check"
    else
      echo "------------------------------------------------------------"
      echo "2: Survey server is on press any key to exit."
    cd ..
    read -n 1 -s -r -p "Press any key to continue"

    fi

fi

