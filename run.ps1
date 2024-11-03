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

python -m venv ./backend/venv
& .\backend\venv\Scripts\activate.bat
& .\backend\venv\Scripts\Activate.ps1

# jason had issues with this lines, I added new lines to force it to work
& ./backend/venv/Scripts/pip install -r ./backend/requirements.txt
& pip install -r ./backend/requirements.txt
& ./backend/venv/Scripts/python ./backend/createdb.py
& python ./backend/createdb.py

& npm update --prefix ./frontend
& npm install --prefix ./frontend

$workingDirectory = Get-Location
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "./backend/venv/Scripts/python ./backend/src/app.py" -WorkingDirectory $workingDirectory
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "npm start --prefix ./frontend" -WorkingDirectory $workingDirectory

