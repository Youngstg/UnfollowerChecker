#!/bin/bash
# Instagram Unfollower Checker - Development Helper Script
# Usage: ./dev.sh <command>

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

show_help() {
    echo -e "${CYAN}Instagram Unfollower Checker - Commands${NC}"
    echo ""
    echo -e "${YELLOW}Setup:${NC}"
    echo "  ./dev.sh install    - Install dependencies dengan uv"
    echo "  ./dev.sh dev        - Install dengan dev dependencies"
    echo "  ./dev.sh env        - Setup .env file"
    echo ""
    echo -e "${YELLOW}Run:${NC}"
    echo "  ./dev.sh run        - Run development server"
    echo "  ./dev.sh prod       - Run production server (gunicorn)"
    echo ""
    echo -e "${YELLOW}Maintenance:${NC}"
    echo "  ./dev.sh clean      - Clean cache dan temporary files"
    echo "  ./dev.sh test       - Run tests"
    echo "  ./dev.sh lint       - Run linter"
    echo "  ./dev.sh format     - Format code dengan black"
    echo ""
    echo -e "${YELLOW}Database:${NC}"
    echo "  ./dev.sh db-backup  - Backup database"
    echo "  ./dev.sh db-clean   - Clean database"
    echo ""
}

install_deps() {
    echo -e "${GREEN}Installing dependencies...${NC}"
    uv sync
}

install_dev() {
    echo -e "${GREEN}Installing with dev dependencies...${NC}"
    uv sync --extra dev
}

setup_env() {
    if [ -f .env ]; then
        echo -e "${YELLOW}.env already exists${NC}"
    else
        echo -e "${GREEN}Copying .env.example to .env...${NC}"
        cp .env.example .env
        echo -e "${CYAN}Please edit .env file with your configuration${NC}"
        ${EDITOR:-nano} .env
    fi
}

run_app() {
    echo -e "${GREEN}Starting development server...${NC}"
    echo -e "${CYAN}Open browser: http://localhost:5000${NC}"
    uv run python app.py
}

run_prod() {
    echo -e "${GREEN}Starting production server with gunicorn...${NC}"
    uv run gunicorn -w 4 -b 0.0.0.0:5000 app:app
}

clean_project() {
    echo -e "${YELLOW}Cleaning cache and temporary files...${NC}"
    rm -rf __pycache__ .pytest_cache
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name "*.log" -delete
    echo -e "${GREEN}Cleaned!${NC}"
}

run_tests() {
    echo -e "${GREEN}Running tests...${NC}"
    uv run pytest
}

run_lint() {
    echo -e "${GREEN}Running linter...${NC}"
    uv run flake8 app.py
}

format_code() {
    echo -e "${GREEN}Formatting code with black...${NC}"
    uv run black app.py
}

backup_db() {
    if [ -f unfollower_tracker.db ]; then
        timestamp=$(date +%Y%m%d_%H%M%S)
        backup_file="unfollower_tracker.db.backup_${timestamp}"
        cp unfollower_tracker.db "$backup_file"
        echo -e "${GREEN}Database backed up to $backup_file${NC}"
    else
        echo -e "${YELLOW}No database found${NC}"
    fi
}

clean_db() {
    echo -e "${RED}WARNING: This will delete all data!${NC}"
    read -p "Are you sure? (y/n): " confirm
    if [ "$confirm" = "y" ]; then
        rm -f unfollower_tracker.db
        echo -e "${YELLOW}Database deleted${NC}"
    else
        echo -e "${GREEN}Cancelled${NC}"
    fi
}

# Main switch
case "${1:-help}" in
    help)
        show_help
        ;;
    install)
        install_deps
        ;;
    dev)
        install_dev
        ;;
    env)
        setup_env
        ;;
    run)
        run_app
        ;;
    prod)
        run_prod
        ;;
    clean)
        clean_project
        ;;
    test)
        run_tests
        ;;
    lint)
        run_lint
        ;;
    format)
        format_code
        ;;
    db-backup)
        backup_db
        ;;
    db-clean)
        clean_db
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
