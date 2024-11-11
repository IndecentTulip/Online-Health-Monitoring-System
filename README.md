# Jlabssssss
```
.
├── backend/
├── database/
├── frontend/
├── Project_Documentation/
│   ├── class_design/
│   ├── database_design/
│   ├── dataflow_planing/
│   ├── flowchart_planing/
│   ├── results.drawio/
│   ├── sequence_design/
│   ├── Team1_SDD_info_2413.pdf
│   ├── Team1_SRS_Info_2413.pdf
│   └── usecases_planing/
└── README.md
```

> NOTE THAT YOU WILL NEED TO RUN BACKEND AND FRONTEND IS DIFFERENT TERMINALS

poweshell:
```
    .\run.ps1
```
bash:
```
    ./run.sh
```


by hand

## build database

    cd ./database/

    psql

    CREATE USER <username> WITH PASSWORD <password>;


    ```Init database schema
    psql -U <username> -d postgres < schema.sql

    ```

    ```Seed database
    psql -U <username> -d jlabs < seed.sql
    ```

## start backend

    cd ./backend/

    python -m venv venv

    ```cmd
    venv\Scripts\activate
    ```

    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

    pip install -r requirements.txt

    python app.py


> If can't, just do

    .\venv\Scripts\python app.py

## start frontend

    cd ./frontend/

    npm install

    npm start
