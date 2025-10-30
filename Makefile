.PHONY: help setup build up down logs clean test deploy ci

help:
	@echo "AI Merchandising System - Available Commands:"
	@echo "  make setup    - Install dependencies for all services"
	@echo "  make build    - Build all Docker images"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make logs     - View logs from all services"
	@echo "  make clean    - Remove containers, volumes, and images"
	@echo "  make test     - Run tests for all services"
	@echo "  make deploy   - (disabled) GCP deploy placeholder"
	@echo "  make ci       - CI-friendly build and tests (no cloud)"

setup:
	@echo "Setting up development environment..."
	cd frontend && npm install
	cd backend && composer install
	cd ml_service && pip install -r requirements.txt
	cd cloud_functions && pip install -r requirements.txt

build:
	@echo "Building Docker images..."
	docker compose build

up:
	@echo "Starting services..."
	docker compose up -d

down:
	@echo "Stopping services..."
	docker compose down

logs:
	docker compose logs -f

clean:
	@echo "Cleaning up..."
	docker compose down -v --remove-orphans
	docker system prune -f

test:
	@echo "Running tests..."
	cd ml_service && pytest
	cd backend && php artisan test

deploy:
	@echo "GCP deployment is disabled. No action taken."
	@echo "Set up an alternative deploy (e.g., Render, Fly.io) or enable GCP later."

ci:
	@echo "Running CI steps (no cloud auth)..."
	make setup
	make test
	make build

