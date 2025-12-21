.PHONY: help install dev run clean test lint format

help:
	@echo "Instagram Unfollower Checker - Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install    - Install dependencies dengan uv"
	@echo "  make dev        - Install dengan dev dependencies"
	@echo "  make env        - Setup .env file"
	@echo ""
	@echo "Run:"
	@echo "  make run        - Run development server"
	@echo "  make prod       - Run production server (gunicorn)"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean      - Clean cache dan temporary files"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linter"
	@echo "  make format     - Format code dengan black"
	@echo ""
	@echo "Database:"
	@echo "  make db-backup  - Backup database"
	@echo "  make db-clean   - Clean database"

install:
	uv sync

dev:
	uv sync --extra dev

env:
	@if not exist .env ( \
		echo Copying .env.example to .env... && \
		copy .env.example .env && \
		echo Please edit .env file with your configuration \
	) else ( \
		echo .env already exists \
	)

run:
	uv run python app.py

prod:
	uv run gunicorn -w 4 -b 0.0.0.0:5000 app:app

clean:
	-rmdir /s /q __pycache__
	-rmdir /s /q .pytest_cache
	-del /q *.pyc
	-del /q *.pyo
	-del /q *.log

test:
	uv run pytest

lint:
	uv run flake8 app.py

format:
	uv run black app.py

db-backup:
	@echo Backing up database...
	@if exist unfollower_tracker.db ( \
		copy unfollower_tracker.db unfollower_tracker.db.backup && \
		echo Database backed up to unfollower_tracker.db.backup \
	) else ( \
		echo No database found \
	)

db-clean:
	@echo WARNING: This will delete all data!
	@set /p confirm="Are you sure? (y/n): "
	@if "%confirm%"=="y" del unfollower_tracker.db
