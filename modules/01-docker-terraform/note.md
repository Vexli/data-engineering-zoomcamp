# 1 Docker & Terraform

## 1.2 Docker

### Learning Questions

1. What is docker?
2. Why do we need it?
3. How to run postgres locally with doker
4. How do we put some data for testing into local postgres with Python?
5. How to package this script in docker?
6. How to run postgres and the script in one network?
7. How to compose and run pgadmin and postres together with `docker-compose`?

### [1.2.1 Introduction](https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=5)

#### Docker

-   Docker is a program that allows you to install and run programs within it in a compartmentalized fashion.
-   You can save the environment as images which allow you to easily save and redeploy the same setup across different environments (e.g. Cloud, quality, production, etc.)
-   Allows you to reproduce and test pipelines easily without affecting the live instance
-   To exit Python in Docker, press `ctrl+D`
-   To install a Python module in docker, you must enter python with bash
    -   `docker run -it --entrypoint=bash python:3.9`
-   When starting the Python container again, it will not have our previously imported libraries by default
    -   It gets the previous state
-   Build image with `docker build -t <IMAGE:VERSION> .`
    -   `dockerfil` will have the setup instructions
-   Run specific image with `docker run -it <IMAGE:VERSION>`
    -   `-it` allows the container to be stopped

#### [1.2.2 Ingesting NY Taxi Data to Postgres](https://www.youtube.com/watch?v=2JM-ziJt0WI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=7)

-   install postgress via docker, based off the [yaml](https://hub.docker.com/_/postgres)

```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v ny_taxi_postgres_data:{PATH_PROJECT}/data-engineering-zoomcamp/project/ny_taxi_postgres_data \
    -p 5432:5432 \
    postgres:13
```

-   `pgcli` accesses postgres via a CLI
    -   connect via `pgcli -h localhost -p 5432 -u root -d ny_taxi`
-   grab the Yellow Taxi data with `wget`
    -   `wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz`
-   find docker containers with `docker ps`

#### [1.2.3 Connecting `pgAdmin` and Postgres](https://www.youtube.com/watch?v=hCAIVe9N0ow&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=7)

-   Get pgAdmin
    -   `docker pull dpage/pgadmin4`
    -   use `ctrl+c` to quit

```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    dpage/pgadmin4
```

-   how do we connect localhost and container?
    -   put them in the same network
        -   `docker network create pg-network`

```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v ny_taxi_postgres_data:/home/gexli/Documents/Project/code/data-engineering-zoomcamp/project/ny_taxi_postgres_data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13
```

```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
```

-   you can remove containers with `docker rm <CONTAINER>`

#### [1.2.4 Dockerizing the Ingestion Script](https://www.youtube.com/watch?v=B1WwATwf-vY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=8)
