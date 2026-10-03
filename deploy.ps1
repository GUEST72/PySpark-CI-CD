$ErrorActionPreference = "Stop"

# Force PySpark to use the Windows Python executable
$env:PYSPARK_PYTHON = "python"
$env:PYSPARK_DRIVER_PYTHON = "python"

Write-Host "Starting deployment..."

Write-Host "Current commit:"
git rev-parse --short HEAD

Write-Host "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Running tests..."
pytest

Write-Host "Running PySpark application..."
python run_job.py

Write-Host "Deployment completed successfully."