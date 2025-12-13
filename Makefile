.PHONY: help install build build-chrome build-firefox dev clean docker-build docker-run docker-shell test backend-install backend-rebuild backend-dev backend-stop api-test test-unit test-integration test-functional test-all test-coverage test-watch test-ci test-local-unit test-local-all start stop

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
	@echo "  make start            Start EVERYTHING (backend + DB + frontend)"
	@echo "  make stop             Stop everything"
	@echo "  make dev              Start extension dev server only"
	@echo "  make backend-dev      Start backend + DB only"
	@echo "  make backend-rebuild  Rebuild backend Docker image (after deps change)"
	@echo "  make backend-stop     Stop backend + DB"
	@echo "  make docker-shell     Open shell in container"
	@echo ""
	@echo "API:"
	@echo "  make api-test         Test API endpoints"
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

test:
	@echo "🧪 Running tests..."
	@echo "⚠️  No tests configured yet"
