# Instagram Unfollower Checker - Development Helper Script
# Usage: .\dev.ps1 <command>

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Instagram Unfollower Checker - Commands" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Setup:" -ForegroundColor Yellow
    Write-Host "  .\dev.ps1 install    - Install dependencies dengan uv"
    Write-Host "  .\dev.ps1 dev        - Install dengan dev dependencies"
    Write-Host "  .\dev.ps1 env        - Setup .env file"
    Write-Host ""
    Write-Host "Run:" -ForegroundColor Yellow
    Write-Host "  .\dev.ps1 run        - Run development server"
    Write-Host "  .\dev.ps1 prod       - Run production server (gunicorn)"
    Write-Host ""
    Write-Host "Maintenance:" -ForegroundColor Yellow
    Write-Host "  .\dev.ps1 clean      - Clean cache dan temporary files"
    Write-Host "  .\dev.ps1 test       - Run tests"
    Write-Host "  .\dev.ps1 lint       - Run linter"
    Write-Host "  .\dev.ps1 format     - Format code dengan black"
    Write-Host ""
    Write-Host "Database:" -ForegroundColor Yellow
    Write-Host "  .\dev.ps1 db-backup  - Backup database"
    Write-Host "  .\dev.ps1 db-clean   - Clean database"
    Write-Host ""
}

function Install-Dependencies {
    Write-Host "Installing dependencies..." -ForegroundColor Green
    uv sync
}

function Install-Dev {
    Write-Host "Installing with dev dependencies..." -ForegroundColor Green
    uv sync --extra dev
}

function Setup-Env {
    if (Test-Path .env) {
        Write-Host ".env already exists" -ForegroundColor Yellow
    } else {
        Write-Host "Copying .env.example to .env..." -ForegroundColor Green
        Copy-Item .env.example .env
        Write-Host "Please edit .env file with your configuration" -ForegroundColor Cyan
        notepad .env
    }
}

function Run-App {
    Write-Host "Starting development server..." -ForegroundColor Green
    Write-Host "Open browser: http://localhost:5000" -ForegroundColor Cyan
    uv run python app.py
}

function Run-Prod {
    Write-Host "Starting production server with gunicorn..." -ForegroundColor Green
    uv run gunicorn -w 4 -b 0.0.0.0:5000 app:app
}

function Clean-Project {
    Write-Host "Cleaning cache and temporary files..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue
    Remove-Item -Force *.pyc -ErrorAction SilentlyContinue
    Remove-Item -Force *.pyo -ErrorAction SilentlyContinue
    Remove-Item -Force *.log -ErrorAction SilentlyContinue
    Write-Host "Cleaned!" -ForegroundColor Green
}

function Run-Tests {
    Write-Host "Running tests..." -ForegroundColor Green
    uv run pytest
}

function Run-Lint {
    Write-Host "Running linter..." -ForegroundColor Green
    uv run flake8 app.py
}

function Format-Code {
    Write-Host "Formatting code with black..." -ForegroundColor Green
    uv run black app.py
}

function Backup-Database {
    if (Test-Path unfollower_tracker.db) {
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $backupFile = "unfollower_tracker.db.backup_$timestamp"
        Copy-Item unfollower_tracker.db $backupFile
        Write-Host "Database backed up to $backupFile" -ForegroundColor Green
    } else {
        Write-Host "No database found" -ForegroundColor Yellow
    }
}

function Clean-Database {
    Write-Host "WARNING: This will delete all data!" -ForegroundColor Red
    $confirm = Read-Host "Are you sure? (y/n)"
    if ($confirm -eq 'y') {
        Remove-Item unfollower_tracker.db -ErrorAction SilentlyContinue
        Write-Host "Database deleted" -ForegroundColor Yellow
    } else {
        Write-Host "Cancelled" -ForegroundColor Green
    }
}

# Main switch
switch ($Command) {
    "help" { Show-Help }
    "install" { Install-Dependencies }
    "dev" { Install-Dev }
    "env" { Setup-Env }
    "run" { Run-App }
    "prod" { Run-Prod }
    "clean" { Clean-Project }
    "test" { Run-Tests }
    "lint" { Run-Lint }
    "format" { Format-Code }
    "db-backup" { Backup-Database }
    "db-clean" { Clean-Database }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
    }
}
