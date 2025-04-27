#!/usr/bin/bash
set -e # exit immediately on error

# generates key + cert in shared folder
# TO BE USED ONLY IN DEV ENV!
DESTINATION="shared"
KEY=$DESTINATION/dev_cert.pem
CERT=$DESTINATION/dev_key.pem
DATETIME=$(date "+%Y-%m-%dt%H_%M_%S")

if [[ -f $KEY && -f $CERT ]]; then
    echo "'$KEY' and  '$CERT' already exist. Skipping the key + cert creation."
else
    echo "Creating '$KEY' and  '$CERT'."
    openssl req -x509 \
        -newkey rsa:4096 -nodes \
        -out $KEY \
        -keyout $CERT \
        -days 365 \
        -subj "/CN=localhost"
fi

# TODO: create better solution for running migration on the start of backend
# running migrations (sleep is needed in order to connect to DB)
docker compose -f dev.docker-compose.yaml up --detach && sleep 1 && \
docker exec --workdir /backend -it typer-backend-1 bash -c "alembic upgrade head"