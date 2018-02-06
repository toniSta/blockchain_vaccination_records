#!/usr/bin/env bash
docker stop a4 a5 d3
docker container prune -f
docker volume prune -f