.PHONY: help install build build-chrome build-firefox dev clean docker-build docker-run docker-shell test

DOCKER_IMAGE := offer-search
DOCKER_TAG := latest

help:
	@echo "Offer Search - Makefile Commands"
	@echo "=================================="
	@echo ""
	@echo "Installation:"
	@echo "  make install          Install dependencies (local)"
	@echo "  make docker-build     Build Docker image"
	@echo ""
	@echo "Build:"
	@echo "  make build            Build extension for Chrome (local)"
	@echo "  make build-chrome     Build extension for Chrome (local)"
	@echo "  make build-firefox    Build extension for Firefox (local)"
	@echo "  make docker-run       Build extension using Docker"
	@echo ""
	@echo "Development:"
	@echo "  make dev              Start Vite dev server"
	@echo "  make docker-shell     Open shell in Docker container"
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

test:
	@echo "🧪 Running tests..."
	@echo "⚠️  No tests configured yet"
