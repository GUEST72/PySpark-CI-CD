$ErrorActionPreference = "Stop"

$Python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    Write-Error "Python virtual environment was not found: $Python"
    exit 1
}

Write-Host "Using Python:"
& $Python --version

$env:PYSPARK_PYTHON = $Python
$env:PYSPARK_DRIVER_PYTHON = $Python

Write-Host "Starting deployment..."

Write-Host "Current commit:"
git rev-parse --short HEAD

Write-Host "Running PySpark application..."
& $Python run_job.py

if ($LASTEXITCODE -ne 0) {
    Write-Error "PySpark application failed."
    exit $LASTEXITCODE
}

Write-Host "Deployment completed successfully."
