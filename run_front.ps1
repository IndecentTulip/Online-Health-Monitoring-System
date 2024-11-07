
cd ./frontend/
& npm install
cd ..

Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "cd ./frontend/ ; npm start" -WorkingDirectory $workingDirectory
