
& npm install --prefix ./frontend

Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "npm start --prefix ./frontend" -WorkingDirectory $workingDirectory
