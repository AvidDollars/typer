#!/usr/bin/env bash
set -e # exit immediately on error

# generates key + cert in shared folder
# TO BE USED ONLY IN DEV ENV!
DESTINATION="./shared"
KEY=$DESTINATION/dev_cert.pem
CERT=$DESTINATION/dev_key.pem

DEV_ENV_FILE=".env.dev"
BACKEND_APP_PATH="./backend/app"
BACKEND_ENV_FILE="$BACKEND_APP_PATH/.env.yml"
BACKEND_SAMPLE_ENV_FILE="$BACKEND_APP_PATH/sample.env.yml"
EMAIL_REGEX="^[a-z0-9!#\$%&'*+/=?^_\`{|}~-]+(\.[a-z0-9!#$%&'*+/=?^_\`{|}~-]+)*@([a-z0-9]([a-z0-9-]*[a-z0-9])?\.)+[a-z0-9]([a-z0-9-]*[a-z0-9])?\$"

function fn_exit_on_missing_dependency() {
    [[ $# -eq 0 ]] && echo "no argument provided" && exit 1

    for dependency in "$@"; do
        command -v $dependency >/dev/null 2>&1 || \
        (echo "'$dependency' is not installed" && exit 1)
    done
}

# creates self-signed SSL cert if missing
function fn_init_ssl_cert() {
    mkdir -p "$DESTINATION"

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

function fn_remove_dev_env_file() {
    rm "$DEV_ENV_FILE"
    exit 69
}

function fn_create_env_file() {
    # remove file if the process is aborted
    trap fn_remove_dev_env_file SIGTERM
    trap fn_remove_dev_env_file SIGINT
    trap fn_remove_dev_env_file SIGKILL

    echo "Missing '$DEV_ENV_FILE'. You will be prompted to provided missing information to generate the file."

    # DB PASSWORD
    read -p "Enter DB password: " POSTGRES_PASSWORD
    echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> $DEV_ENV_FILE

    # DB USER
    read -p "Enter DB user: " POSTGRES_USER
    echo "POSTGRES_USER=$POSTGRES_USER" >> $DEV_ENV_FILE

    # DB NAME
    echo "POSTGRES_DB=typer" >> $DEV_ENV_FILE

    # EMAIL FOR PGADMIN
    read -p "Enter your email: " PGADMIN_DEFAULT_EMAIL
    while [[ ! $PGADMIN_DEFAULT_EMAIL =~ $EMAIL_REGEX ]]; do
        read -p "Invalid input. Enter valid email: " PGADMIN_DEFAULT_EMAIL
    done
    echo "PGADMIN_DEFAULT_EMAIL=$PGADMIN_DEFAULT_EMAIL" >> $DEV_ENV_FILE

    # PGADMIN PASSWORD
    echo "PGADMIN_DEFAULT_PASSWORD=$POSTGRES_PASSWORD" >> $DEV_ENV_FILE
}

function fn_create_backend_env_file() {

    # load contents of DEV ENV file
    declare -A dev_env
    while IFS='=' read -r key value; do
        dev_env[$key]=$value
    done < "./$DEV_ENV_FILE"

    # create backend ENV file from the sample file
    cp $BACKEND_SAMPLE_ENV_FILE $BACKEND_ENV_FILE
    chmod 600 $BACKEND_ENV_FILE

    # contents of DEV ENV file
    local USER="${dev_env[POSTGRES_USER]}"
    local PASSWORD="${dev_env[POSTGRES_PASSWORD]}"
    local DB_NAME="${dev_env[POSTGRES_DB]}"
    local DB_URL="db_url: postgresql+asyncpg://$USER:$PASSWORD@db:5432/$DB_NAME"

    # populate backend ENV file with secrets
    sed -i "/^db_url/c $DB_URL" $BACKEND_ENV_FILE
    sed -i "/^secret/c secret: $(python3 -c 'import secrets; print(secrets.token_hex(32))')" $BACKEND_ENV_FILE
    sed -i "/^pepper/c pepper: $(python3 -c 'import secrets; print(secrets.token_hex(4))')" $BACKEND_ENV_FILE
    sed -i "/^refresh_token_secret/c refresh_token_secret: $(python3 -c 'import secrets; print(secrets.token_hex(32))')" $BACKEND_ENV_FILE
}

#################################################################################
############################## INIT DEV ENV #####################################
#################################################################################

# create DEV env file if missing
if [[ ! -f $DEV_ENV_FILE ]]; then
    fn_create_env_file    
fi

# create backend env file if missing
if [[ ! -f $BACKEND_ENV_FILE ]]; then
    echo "Generating missing '$BACKEND_ENV_FILE' file."
    fn_create_backend_env_file
fi

fn_exit_on_missing_dependency openssl docker docker-compose python3
fn_init_ssl_cert

# running migrations (sleep is needed in order to connect to DB)
docker compose -f dev.docker-compose.yaml up --detach && sleep 1 && \
docker exec --workdir /backend -it typer-backend-1 bash -c "alembic upgrade head"
#################################################################################
