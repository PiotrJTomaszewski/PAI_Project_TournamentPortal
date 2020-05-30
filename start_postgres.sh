#!/bin/bash
docker run -i \
    -p 5432:5432 \
    --name tournamentAppDevDB \
    -e POSTGRES_USER="dev" \
    -e POSTGRES_PASSWORD="dev" \
    -e POSTGRES_DB="tournamentAppDev" \
    postgres