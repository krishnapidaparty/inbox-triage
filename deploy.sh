#!/bin/bash

# Production Deployment Script for Inbox Triage Assistant
set -e

echo "🚀 Starting production deployment..."

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run as root"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Set environment variables
export SECRET_KEY=${SECRET_KEY:-$(openssl rand -hex 32)}
export GOOGLE_CREDENTIALS_FILE=${GOOGLE_CREDENTIALS_FILE:-credentials.json}

echo "🔧 Environment variables set:"
echo "   SECRET_KEY: ${SECRET_KEY:0:16}..."
echo "   GOOGLE_CREDENTIALS_FILE: $GOOGLE_CREDENTIALS_FILE"

# Check if credentials file exists
if [ ! -f "$GOOGLE_CREDENTIALS_FILE" ]; then
    echo "⚠️  Warning: $GOOGLE_CREDENTIALS_FILE not found."
    echo "   The app will run in demo mode without Gmail integration."
    echo "   To enable Gmail integration, place your credentials.json file in the project root."
fi

# Create logs directory
mkdir -p logs

# Build and start services
echo "📦 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services are running!"
    echo "🌐 Application URL: http://localhost:8080"
    echo "📊 Health check: http://localhost:8080/api/status"
    
    # Show logs
    echo "📋 Recent logs:"
    docker-compose logs --tail=20
else
    echo "❌ Services failed to start. Check logs:"
    docker-compose logs
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo ""
echo "📝 Next steps:"
echo "   1. Access your application at http://localhost:8080"
echo "   2. Monitor logs: docker-compose logs -f"
echo "   3. Stop services: docker-compose down"
echo "   4. Update application: git pull && docker-compose up -d --build"
