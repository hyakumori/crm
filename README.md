# MAMORI crm

![pipeline](https://gitlab.com/datafluct/hyakumori_crm/badges/develop/pipeline.svg)

## Requirements

- Python>=3.7 (consider using `pyenv` to manage python version).

- Vuejs

- Postgresql>=11

## Installation

### Postgres

- Start postgres service with docker

```
$ docker service create --name postgres11 \
    --mount type=volume,source=postgres11,destination=/var/lib/postgresql/data \
    -e POSTGRES_PASSWORD=masterpassword \
    --publish 5432:5432 \
    postgres:11-alpine
```

- Run `psql` client in postgres container to create user and database

```
$ docker exec -ti [containerid] psql -U postgres

postgres=# CREATE ROLE mamori WITH PASSWORD 'mypassword' LOGIN CREATEDB;

postgres=# CREATE DATABASE mamori OWNER mamori;
```

### Python

- Create virtualenv: `python -m venv venv`

- Activate virtualenv: `source venv/bin/activate`

- Update `pip` and `setuptools`: `pip install -U pip setuptools`

- Install `pip-tools`: `pip install pip-tools`

### Run on local

1. Install once with `MAMORI_LIGHT_BUILD=1 pip install -e .[dev]`
2. Copy `.env.example` to `.env` and fill necessary variables for both backend and fontend.
3. [FRONTEND] Move to `mamori/static/mamori` run `yarn`
4. Run dev server with `STATIC_DIR="" mamori runserver`. You might want to set `STATIC_DIR=""` in `.env`.

### Dependency management

#### Front-end

Using `yarn`.

#### Backend

Using `pip-tools`

**Runtime**

- Add a dependeny to requirements.in, consider pin its version.

- Compile to `requirements.txt`: `pip-compile --generate-hashes setup.py`

**Dev**

- Add a dependeny to requirements-dev.in, consider pin its version.

- Compile to `requirements-dev.txt`: `pip-compile requirements-dev.in`

Remember to reinstall package.
