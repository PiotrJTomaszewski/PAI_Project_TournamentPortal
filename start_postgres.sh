#!/bin/bash
docker run -d \
    --network bridge \
    -p 5432:5432 \
    --name tournamentAppDevDB \
    -e POSTGRES_USER="dev" \
    -e POSTGRES_PASSWORD="dev" \
    -e POSTGRES_DB="tournamentAppDev" \
    postgres
