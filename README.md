# Jlabs

```
.
├── !Demo!
│   ├── backend/
│   ├── database/
│   └── frontend/
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

## build database

    cd ./database/

    ```Init database schema
    psql -U <username> -d postgres < schema.sql
    ```

    ```Seed database
    psql -U <username> -d jlabs < seed.sql
    ```

## start backend

    cd ./backend/

    ```cmd
    venv\Scripts\activate
    ```

    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

    python app.py


> If can't, just do

    .\venv\Scripts\python app.py

## start frontend

    cd ./frontend/

    npm start


