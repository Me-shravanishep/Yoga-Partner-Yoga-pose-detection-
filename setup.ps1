param(
    [string]$Python = "py -3.10"
)

Write-Host "Using Python command: $Python"

& $Python -m venv venv
& .\venv\Scripts\python.exe -m pip install --upgrade pip
& .\venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Setup complete. Activate with: .\\venv\\Scripts\\Activate.ps1"
