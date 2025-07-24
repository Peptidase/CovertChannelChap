#!/bin/bash

docker compose down -v --remove-orphans
docker container prune -f
docker network prune -f
docker volume prune -f
