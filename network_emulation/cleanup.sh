#!/bin/bash
# Cleanup Docker Compose resources

docker compose down --volumes --remove-orphans
docker container prune -f
docker image prune -a -f
docker volume prune -f
docker network prune -f

docker network ls -q | xargs -r docker network rm