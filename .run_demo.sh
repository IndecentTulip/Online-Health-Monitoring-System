#!/bin/bash

echo "Startig Jlabs"

ls ./Demo/database/

#psql -U <username> -d postgres < schema.sql
#psql -U <username> -d jlabs < seed.sql

ls ./Demo/backend
echo "database user:"
read user
echo "database password:"
read password 

rm -rf ./Demo/backend/venv_linux/
rm -rf ./Demo/backend/src/credentials.txt

touch ./Demo/backend/src/credentials.txt
echo "user=$user" >> ./Demo/backend/src/credentials.txt
echo "password=$password" >> ./Demo/backend/src/credentials.txt

python -m venv ./Demo/backend/venv_linux
./Demo/backend/venv_linux/bin/pip install -r ./Demo/backend/requirements.txt
./Demo/backend/venv_linux/bin/python ./Demo/backend/src/app.py &

ls ./Demo/frontend/

npm update --prefix ./Demo/frontend

npm install --prefix ./Demo/frontend

npm start --prefix ./Demo/frontend &
