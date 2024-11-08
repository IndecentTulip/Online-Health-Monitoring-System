# PowerShell Script
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

Write-Host "Starting Jlabs"

function Check-Command {
    param (
        [string]$commandName
    )
    if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
        Write-Host "$commandName is not installed or not found in PATH. Exiting script."
        exit 1
    }
}
Check-Command python
Check-Command node

$user = Read-Host -Prompt "Database user"
$password = Read-Host -Prompt "Database password"

Remove-Item -Path "./backend/src/credentials.txt" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "./backend/venv/" -Recurse -Force -ErrorAction SilentlyContinue

New-Item -Path "./backend/src/credentials.txt" -ItemType File -Force
Add-Content -Path "./backend/src/credentials.txt" -Value "user=$user"
Add-Content -Path "./backend/src/credentials.txt" -Value "password=$password"


cd ./backend/
python -m venv venv
cd .. 
& .\backend\venv\Scripts\activate.bat
& .\backend\venv\Scripts\Activate.ps1

pip install --upgrade pip setuptools wheel

# Ensure the backend dependencies are installed
if (-not (& ./backend/venv/Scripts/pip install -r ./backend/requirements.txt)) {
    # If the first command fails, run the second one
    & pip install -r ./backend/requirements.txt
    & pip uninstall psycopg2
    & pip install psycopg2-binary
}

# Create the database for the backend (run the createdb script)
if (-not (& ./backend/venv/Scripts/python ./backend/createdb.py)) {
    # If the first command fails, run the second one
    & python ./backend/createdb.py
}
cd ./frontend/
& npm update
& npm install
cd ..

$workingDirectory = Get-Location

Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "./backend/venv/Scripts/python ./backend/src/app.py" -WorkingDirectory $workingDirectory

# Open another new terminal and run the frontend application
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "npm start --prefix ./frontend" -WorkingDirectory $workingDirectory

