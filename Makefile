.PHONY: help install dev test lint format docker-up docker-down clean

help:
	@echo "SmartTourism City Guide - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install all dependencies"
	@echo "  make dev           Start development environment"
	@echo ""
	@echo "Testing:"
	@echo "  make test          Run all tests"
	@echo "  make lint          Check code style"
	@echo "  make format        Format code (black, prettier)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up     Start Docker services"
	@echo "  make docker-down   Stop Docker services"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean         Clean cache files"

install:
	@echo "Installing Python dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing Node dependencies..."
	cd frontend && npm install
	@echo "✓ All dependencies installed"

dev:
	@echo "Starting development environment..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo "Press Ctrl+C to stop"
	@echo ""
	@(cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &) && \
	(cd frontend && npm run dev &) && \
	wait

dev-backend:
	cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

test:
	@echo "Running tests..."
	cd backend && pytest -v
	cd frontend && npm test -- --coverage

lint:
	@echo "Linting Python code..."
	cd backend && flake8 . --max-line-length=100
	@echo "Linting JavaScript code..."
	cd frontend && npm run lint
	@echo "✓ All code checked"

format:
	@echo "Formatting Python code..."
	cd backend && black .
	@echo "Formatting JavaScript code..."
	cd frontend && npm run format
	@echo "✓ All code formatted"

docker-up:
	@echo "Starting Docker services..."
	docker-compose -f config/docker-compose.yml up -d
	@echo "✓ Services running"
	@echo "Orion CB: http://localhost:1026"
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo "TimescaleDB: localhost:5432"

docker-down:
	@echo "Stopping Docker services..."
	docker-compose -f config/docker-compose.yml down
	@echo "✓ Services stopped"

docker-logs:
	docker-compose -f config/docker-compose.yml logs -f

clean:
	@echo "Cleaning cache files..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "node_modules" -not -path "./frontend/node_modules" -exec rm -rf {} +
	cd frontend && rm -rf dist build
	@echo "✓ Cache cleaned"
