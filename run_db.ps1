& .\backend\venv\Scripts\activate.bat
& .\backend\venv\Scripts\Activate.ps1

if (-not (& ./backend/venv/Scripts/python ./backend/createdb.py)) {
    # If the first command fails, run the second one
    & python ./backend/createdb.py
}

