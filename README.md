# TYPER - practise typing with all 10 fingers
Application built on top of [FastAPI](https://fastapi.tiangolo.com/) + [Angular](https://angular.dev/) frameworks and [PostgreSQL](https://www.postgresql.org/) database.


## Initializing DEV environment
DEV environment runs in isolated ligthweight Docker containers orchestrated with Docker Compose.

To initialize DEV environment run the following command:
```bash
# WHAT IT DOES?
#   -   creates essential env files on initial startup
#   -   creates self-signed SSL certificates for frontend and backend
#   -   starts containers defined in "dev.docker-compose.yaml"
#   -   runs migrations for Postgres DB
./run_dev_env.sh
```

After initialization the following URLs will be available:
- [Angular frontend](https://localhost:4200/)
- [FastAPI backend](https://localhost:8000/)
- [pgAdmin UI for database](http://localhost:5050)
    -   for login use **PGADMIN_** variables available in **.env.dev** file which was automatically created from your prompt during first initialization of DEV environment
