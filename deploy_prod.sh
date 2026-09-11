#!/bin/bash

# deploy.sh
set -e

echo "Starting deployment..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo ".env file not found!"
    exit 1
fi

# Pull latest changes (if using git)
# git pull origin main

# Stop existing containers
echo "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

# Build and start containers
echo "Building and starting containers..."
docker-compose -f docker-compose.prod.yml up -d --build

# Run database migrations (if applicable)
echo "Running database migrations..."
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Check container status
echo "Checking container status..."
docker-compose -f docker-compose.prod.yml ps

# Test endpoints
echo "Testing endpoints..."
curl -f http://localhost/health && echo "Backend is healthy"
curl -f http://localhost/ && echo "Frontend is accessible"

echo "Deployment completed successfully!"