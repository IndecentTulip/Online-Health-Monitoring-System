# PowerShell Script
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

Write-Host "Starting Jlabs"

# Function to check if a command exists
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

# Prompt for database user and password
$user = Read-Host -Prompt "Database user"
$password = Read-Host -Prompt "Database password"

# Remove existing credentials and virtual environment
Remove-Item -Path "./backend/src/credentials.txt" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "./backend/venv/" -Recurse -Force -ErrorAction SilentlyContinue

# Create new credentials file
New-Item -Path "./backend/src/credentials.txt" -ItemType File -Force
Add-Content -Path "./backend/src/credentials.txt" -Value "user=$user"
Add-Content -Path "./backend/src/credentials.txt" -Value "password=$password"

# Create Python virtual environment
python -m venv ./backend/venv

# Install requirements
& ./backend/venv/Scripts/pip install -r ./backend/requirements.txt

# Run createdb.py and app.py in new windows
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-File", "./backend/venv/Scripts/python ./backend/createdb.py" -WindowStyle Normal
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-File", "./backend/venv/Scripts/python ./backend/src/app.py" -WindowStyle Normal

# Update and install frontend dependencies
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "npm update --prefix ./frontend" -WindowStyle Normal
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "npm install --prefix ./frontend" -WindowStyle Normal

# Start the frontend app in a new window
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "npm start --prefix ./frontend" -WindowStyle Normal

