.PHONY: help install build build-chrome build-firefox dev clean docker-build docker-run docker-shell test backend-install backend-dev backend-stop api-test test-unit test-integration test-functional test-all test-coverage test-watch test-ci

DOCKER_IMAGE := offer-search
DOCKER_TAG := latest

help:
	@echo "Offer Search - Makefile Commands"
	@echo "=================================="
	@echo ""
	@echo "Installation:"
	@echo "  make install          Install extension dependencies"
	@echo "  make backend-install  Install backend dependencies"
	@echo "  make docker-build     Build Docker images"
	@echo ""
	@echo "Build:"
	@echo "  make build            Build extension for Chrome"
	@echo "  make build-chrome     Build extension for Chrome"
	@echo "  make build-firefox    Build extension for Firefox"
	@echo "  make docker-run       Build extension using Docker"
	@echo ""
	@echo "Development:"
	@echo "  make dev              Start extension dev server"
	@echo "  make backend-dev      Start backend + DB with Docker"
	@echo "  make backend-stop     Stop backend + DB"
	@echo "  make docker-shell     Open shell in container"
	@echo ""
	@echo "Testing:"
	@echo "  make test-unit        Run unit tests only"
	@echo "  make test-integration Run integration tests only"
	@echo "  make test-functional  Run functional/BDD tests only"
	@echo "  make test-all         Run all tests"
	@echo "  make test-coverage    Run all tests with coverage report"
	@echo "  make test-watch       Run tests in watch mode"
	@echo "  make test-ci          Run tests for CI (with coverage XML)"
	@echo "  make api-test         Test API endpoints (manual)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove build artifacts"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	npm install

build: build-chrome

build-chrome:
	@echo "🏗️  Building extension for Chrome..."
	npm run build

build-firefox:
	@echo "🦊 Building extension for Firefox..."
	npm run build
	@echo "📝 Copying Firefox manifest..."
	@if [ -f src/manifest.firefox.json ]; then \
		cp src/manifest.firefox.json dist/manifest.json; \
		echo "✅ Firefox manifest copied"; \
	else \
		echo "⚠️  Firefox manifest not found"; \
	fi

dev:
	@echo "🚀 Starting development server..."
	npm run dev

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf dist/
	rm -rf node_modules/
	@echo "✅ Clean complete"

docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
	@echo "✅ Docker image built: $(DOCKER_IMAGE):$(DOCKER_TAG)"

docker-run:
	@echo "🐳 Building extension in Docker..."
	docker run --rm \
		-v "$(PWD)/dist:/app/dist" \
		$(DOCKER_IMAGE):$(DOCKER_TAG)
	@echo "✅ Build complete in dist/"

docker-shell:
	@echo "🐳 Opening shell in Docker container..."
	docker run --rm -it \
		-v "$(PWD):/app" \
		-w /app \
		$(DOCKER_IMAGE):$(DOCKER_TAG) /bin/sh

backend-install:
	@echo "📦 Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

backend-dev:
	@echo "🚀 Starting backend + database..."
	docker-compose up -d db api
	@echo "✅ Backend running on http://localhost:8000"
	@echo "✅ Database running on localhost:5432"

backend-stop:
	@echo "🛑 Stopping backend + database..."
	docker-compose down

api-test:
	@echo "🧪 Testing API endpoints..."
	@curl -s http://localhost:8000/health | jq . || echo "❌ API not running"
	@curl -s http://localhost:8000/api/jobs/stats | jq . || echo "❌ Stats endpoint failed"

test-unit:
	@echo "🧪 Running unit tests..."
	docker exec offer-search-api-1 python -m pytest -m unit -v

test-integration:
	@echo "🧪 Running integration tests..."
	@echo "⚠️  Ensure database is running (make backend-dev)"
	docker exec offer-search-api-1 python -m pytest -m integration -v

test-functional:
	@echo "🧪 Running functional/BDD tests..."
	@echo "⚠️  Ensure API is running (make backend-dev)"
	docker exec offer-search-api-1 python -m pytest -m functional -v

test-all:
	@echo "🧪 Running all tests..."
	@echo "⚠️  Ensure database and API are running (make backend-dev)"
	docker exec offer-search-api-1 python -m pytest -v

test-coverage:
	@echo "🧪 Running all tests with coverage..."
	@echo "⚠️  Ensure database and API are running (make backend-dev)"
	docker exec offer-search-api-1 python -m pytest -v --cov=app --cov-report=term-missing --cov-report=html
	@echo "📊 Coverage report generated in backend/htmlcov/index.html"

test-watch:
	@echo "🧪 Running tests in watch mode..."
	@echo "⚠️  Ensure database and API are running (make backend-dev)"
	docker exec -it offer-search-api-1 python -m pytest -v --cov=app -f

test-ci:
	@echo "🧪 Running tests for CI..."
	docker exec offer-search-api-1 python -m pytest -v --cov=app --cov-report=xml --cov-report=term --junitxml=junit.xml

test-local-unit:
	@echo "🧪 Running unit tests (local Python)..."
	cd backend && python3 -m pytest -m unit -v

test-local-all:
	@echo "🧪 Running all tests (local Python)..."
	@echo "⚠️  Ensure TEST_DATABASE_URL is set"
	cd backend && python3 -m pytest -v

test: test-all
