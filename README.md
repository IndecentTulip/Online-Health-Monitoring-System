# Jlabs
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

# github link

https://github.com/IndecentTulip/Online-Health-Monitoring-System

# dependencies(programming lenguages)

**For database:**
https://youtu.be/0n41UTkOBb0?si=mwjP3QVn0X90ViIU

https://www.postgresql.org/download/windows/

**For backend:**
https://youtu.be/yivyNCtVVDk?si=YaoqdwUmstb82Udr

https://www.python.org/downloads/

**For frontend:**
https://youtu.be/yOAZDymGWVw?si=R68Jgss3ae-LaECa

https://nodejs.org/en/

https://react.dev/learn/start-a-new-react-project

> NOTE THAT YOU WILL NEED TO RUN BACKEND AND FRONTEND IS DIFFERENT TERMINALS
scripts will open this terminals for you do not be affraid

# project install instractions: 

**To be able to run the scripts**

On Windows
poweshell:
```
Set-ExecutionPolicy Unrestricted
```

**Scripts to run the system**

On Windows
poweshell:
```
.\run.ps1
```

On Linux/Mac
bash:
```
./run.sh
```

by hand

## build database

    cd ./backend/

    ```cmd
    venv\Scripts\activate
    ```

    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
    
    python createdb.py


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


> NOTE If can't source the venv, you can do do
.\venv\Scripts\python app.py

## start frontend

    cd ./frontend/

    npm update 

    npm install

    npm start

# video tutorials

https://youtu.be/7NFysoAMjSs

https://youtu.be/J8InQhY2qks

https://youtu.be/eIRYHYk74Ng

https://youtu.be/wn7Xdk65yS0
