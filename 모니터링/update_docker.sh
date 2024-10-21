#!/bin/sh
echo "Building Docker"

docker-compose -f docker-compose.prod.yml build

echo "Upload Docker"

docker push shinwoohipo/monitoring:latest