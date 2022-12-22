#!/bin/bash

docker system prune -a
docker volume prune
docker-compose build --no-cache
