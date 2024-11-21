# Activate virtual environment (works for both batch and PowerShell)
function Activate-Venv {
    & .\backend\venv\Scripts\Activate.ps1
}

# Show options to the user
$choice = Read-Host "Choose the test to run: (1) Unit Test, (2) Performance Test"

# Activate the virtual environment
Activate-Venv

# Run the appropriate test based on user's choice
if ($choice -eq 1) {
    Write-Host "Running Unit Test..."
    & pytest ./backend/src/API_unit_test.py
}
elseif ($choice -eq 2) {
    Write-Host "Running Performance Test..."
    & locust -f ./backend/src/perfomence_test.py
}
else {
    Write-Host "Invalid choice. Please choose 1 for Unit Test or 2 for Performance Test."
}

