.PHONY: help install build build-chrome build-firefox dev clean docker-build docker-run docker-shell test backend-install backend-rebuild backend-dev backend-stop api-test test-unit test-integration test-functional test-all test-coverage test-watch test-ci test-local-unit test-local-all start stop

DOCKER_IMAGE := offer-search
DOCKER_TAG := latest

help:
	@echo "Offer Search - Makefile Commands"
	@echo "=================================="
	@echo ""
	@echo "Installation:"
	@echo "  make install          Install extension dependencies (optional - auto-installed)"
	@echo "  make backend-install  Install backend dependencies"
	@echo "  make docker-build     Build Docker images"
	@echo ""
	@echo "Build:"
	@echo "  make build            Build extension for Chrome (auto-installs deps)"
	@echo "  make build-chrome     Build extension for Chrome (auto-installs deps)"
	@echo "  make build-firefox    Build extension for Firefox (auto-installs deps)"
	@echo "  make docker-run       Build extension using Docker"
	@echo ""
	@echo "Development:"
	@echo "  make start            Start EVERYTHING (backend + DB + frontend, auto-installs deps)"
	@echo "  make stop             Stop everything"
	@echo "  make dev              Start extension dev server only (auto-installs deps)"
	@echo "  make backend-dev      Start backend + DB only"
	@echo "  make backend-rebuild  Rebuild backend Docker image (after deps change)"
	@echo "  make backend-stop     Stop backend + DB"
	@echo "  make docker-shell     Open shell in container"
	@echo ""
	@echo "Testing:"
	@echo "  make test-unit        Run unit tests only"
	@echo "  make test-integration Run integration tests only"
	@echo "  make test-functional  Run functional/BDD tests only"
	@echo "  make test-all         Run all tests (auto-starts services)"
	@echo "  make test-coverage    Run all tests with coverage (auto-starts services)"
	@echo "  make test-watch       Run tests in watch mode"
	@echo "  make test-ci          Run tests for CI (starts/stops services, with coverage)"
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
	@if [ ! -d "node_modules" ]; then \
		echo "📦 Installing dependencies..."; \
		npm install; \
	fi
	npm run build

build-firefox:
	@echo "🦊 Building extension for Firefox..."
	@if [ ! -d "node_modules" ]; then \
		echo "📦 Installing dependencies..."; \
		npm install; \
	fi
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
	@if [ ! -d "node_modules" ]; then \
		echo "📦 Installing dependencies..."; \
		npm install; \
	fi
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
	@echo "📦 Backend dependencies installation"
	@echo ""
	@echo "🐳 Docker (recommended):"
	@echo "   Dependencies are auto-installed in the Docker image"
	@echo "   Run: make backend-rebuild"
	@echo ""
	@echo "💻 Local installation:"
	@echo "   cd backend && pip3 install -r requirements.txt"
	@echo ""

backend-rebuild:
	@echo "🔨 Rebuilding backend Docker image..."
	docker compose build api
	@echo "✅ Backend image rebuilt with latest dependencies"
	@echo "💡 Run 'make backend-dev' to start the backend"

backend-dev:
	@echo "🚀 Starting backend + database..."
	docker compose up -d db api
	@echo "✅ Backend running on http://localhost:8000"
	@echo "✅ Database running on localhost:5432"

backend-stop:
	@echo "🛑 Stopping backend + database..."
	docker-compose down

start:
	@echo "🚀 Starting ALL services (backend + DB + frontend)..."
	@echo ""
	@if [ ! -d "node_modules" ]; then \
		echo "📦 Installing frontend dependencies..."; \
		npm install; \
		echo ""; \
	fi
	@echo "📦 Step 1/2: Starting backend + database..."
	docker compose up -d db api
	@echo "✅ Backend running on http://localhost:8000"
	@echo "✅ Database running on localhost:5432"
	@echo ""
	@echo "📦 Step 2/2: Starting frontend dev server..."
	@echo "⚠️  Press Ctrl+C to stop the frontend (backend will continue in background)"
	@echo ""
	npm run dev

stop:
	@echo "🛑 Stopping ALL services..."
	@echo "🛑 Stopping backend + database..."
	docker compose down
	@echo "✅ All services stopped"

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
	@echo "📦 Ensuring services are running..."
	@docker compose ps | grep -q "offer-search-api-1" || (echo "🚀 Starting services..." && docker compose up -d db api)
	@echo "⏳ Waiting for services to be ready..."
	@for i in $$(seq 1 30); do \
		if docker exec offer-search-api-1 python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" 2>/dev/null; then \
			break; \
		fi; \
		echo "   Waiting for API ($$i/30)..."; \
		sleep 2; \
	done
	@echo "✅ Services are ready"
	@echo "🧪 Running tests..."
	@docker exec offer-search-api-1 python -m pytest -v || (echo "❌ Tests failed" && exit 1)
	@echo "✅ All tests passed!"

test-coverage:
	@echo "🧪 Running all tests with coverage..."
	@echo "📦 Ensuring services are running..."
	@docker compose ps | grep -q "offer-search-api-1" || (echo "🚀 Starting services..." && docker compose up -d db api)
	@echo "⏳ Waiting for services to be ready..."
	@for i in $$(seq 1 30); do \
		if docker exec offer-search-api-1 python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" 2>/dev/null; then \
			break; \
		fi; \
		echo "   Waiting for API ($$i/30)..."; \
		sleep 2; \
	done
	@echo "✅ Services are ready"
	@echo "🧪 Running tests with coverage..."
	@docker exec offer-search-api-1 python -m pytest -v --cov=app --cov-report=term-missing --cov-report=html
	@echo "📊 Coverage report generated in backend/htmlcov/index.html"

test-watch:
	@echo "🧪 Running tests in watch mode..."
	@echo "⚠️  Ensure database and API are running (make backend-dev)"
	docker exec -it offer-search-api-1 python -m pytest -v --cov=app -f

test-ci:
	@echo "🧪 Running tests for CI..."
	@echo "📦 Starting services..."
	@docker compose up -d db api
	@echo "⏳ Waiting for services to be ready..."
	@for i in $$(seq 1 30); do \
		if docker exec offer-search-api-1 python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" 2>/dev/null; then \
			break; \
		fi; \
		echo "   Waiting for API ($$i/30)..."; \
		sleep 2; \
	done
	@echo "✅ Services are ready"
	@echo "🧪 Running tests with coverage..."
	@docker exec offer-search-api-1 python -m pytest -v --cov=app --cov-report=xml --cov-report=term --junitxml=junit.xml || (echo "❌ Tests failed" && docker compose down && exit 1)
	@echo "✅ Tests passed, stopping services..."
	@docker compose down
	@echo "✅ CI tests completed successfully!"

test-local-unit:
	@echo "🧪 Running unit tests (local Python)..."
	cd backend && python3 -m pytest -m unit -v

test-local-all:
	@echo "🧪 Running all tests (local Python)..."
	@echo "⚠️  Ensure TEST_DATABASE_URL is set"
	cd backend && python3 -m pytest -v

test: test-all
