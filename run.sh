#!/bin/bash

echo "Startig Jlabs"

echo "database user:"
read user
echo "database password:"
read password 

rm -rf ./backend/src/credentials.txt
rm -rf ./backend/venv_linux/

touch ./backend/src/credentials.txt
echo "user=$user" >> ./backend/src/credentials.txt
echo "password=$password" >> ./backend/src/credentials.txt

python -m venv ./backend/venv_linux

./backend/venv_linux/bin/pip install -r ./backend/requirements.txt
./backend/venv_linux/bin/python ./backend/createdb.py
./backend/venv_linux/bin/python ./backend/src/app.py &

npm update --prefix ./frontend

npm install --prefix ./frontend

npm start --prefix ./frontend &

