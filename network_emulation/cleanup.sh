#!/bin/bash


# Stop and remove all Docker containers
docker compose down
docker rm -f $(docker ps -aq) 2>/dev/null || true


# Remove all Docker networks (except default ones)
docker network prune -f

# Note: Volumes are NOT removed
