#!/usr/bin/bash

# running migrations (sleep is needed in order to connect to DB)
docker compose -f dev.docker-compose.yaml up --detach && sleep 1 && \
docker exec --workdir /backend -it typer-backend-1 bash -c "alembic upgrade head"