& .\backend\venv\Scripts\activate.bat
& .\backend\venv\Scripts\Activate.ps1

$workingDirectory = Get-Location
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "./backend/venv/Scripts/python ./backend/src/app.py" -WorkingDirectory $workingDirectory

$workingDirectory = Get-Location
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", ".\backend\venv\Scripts\Activate.ps1; python ./backend/src/app.py" -WorkingDirectory $workingDirectory

