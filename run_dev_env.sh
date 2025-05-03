#!/usr/bin/env bash
set -e # exit immediately on error

# generates key + cert in shared folder
# TO BE USED ONLY IN DEV ENV!
DESTINATION="./shared"
KEY=$DESTINATION/dev_cert.pem
CERT=$DESTINATION/dev_key.pem

function exit_on_missing_dependency() {
    [[ $# -eq 0 ]] && echo "no argument provided" && exit 1

    for dependency in "$@"; do
        command -v $dependency >/dev/null 2>&1 || \
        (echo "'$dependency' is not installed" && exit 1)
    done
}

# creates self-signed SSL cert if missing
function init_ssl_cert() {
    if [[ -f $KEY && -f $CERT ]]; then
        echo "'$KEY' and '$CERT' already exist. Skipping the creation of key and cert."
    else
        echo "Creating '$KEY' and  '$CERT'."
        openssl req -x509 -nodes \
            -newkey rsa:4096 \
            -out $KEY \
            -keyout $CERT \
            -days 365 \
            -subj "/CN=localhost"
    fi
}

exit_on_missing_dependency openssl docker docker-compose
init_ssl_cert
# TODO: create better solution for running migration on the start of backend
# running migrations (sleep is needed in order to connect to DB)
docker compose -f dev.docker-compose.yaml up --detach && sleep 1 && \
docker exec --workdir /backend -it typer-backend-1 bash -c "alembic upgrade head"
