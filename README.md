# Notes BE

A simple notes app with authentication and authorization. 
Rate limiting and audit actions.

⭐️ Swagger on `/docs`

## Feature Description
- Python v3.12
- FastApi BE with JWT authentication
- Mysql, SQLAlchemy and Alembic
- Rate Limiting
- Audit actions
- Work in progress

## Vademecum

### 1. Setup environment (uv)
```shell
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. Configure environment
```shell
cp .env.sample .env
# Edit .env with your values (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE, SECRET_KEY)
```

### 3. Setup database
```shell
# Make sure MySQL is running, then:
mysql -u root -p < sql/create.sql

# Or with Alembic:
alembic upgrade head
```

### 4. Run the project
```shell
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```
App available at `http://localhost:8080` — Swagger at `http://localhost:8080/docs`

### 5. Run tests
```shell
pytest -p no:warnings test/**/*.py
```

### 6. Lint
```shell
pylint app/
```

## Test
```shell
pytest -p no:warnings test/**/*.py
```

## Docker 
- if you use `docker-compose up -d` you can access the app on `localhost:8080` and swagger on `localhost:8080/docs`
- keep in mind that you need to create a `.env` file with the following variables:
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_DATABASE`
- `SECRET_KEY`
  - if you have a demon on machine on port 3306, you need to change the port in the docker-compose.yml file
- If you want to rebuild the image, you need to run the following commands:
  - `docker-compose down`
  - `docker-compose up --build`

## TODOs
 - [x] Add Logger
 - [x] Improve Error Handling
 - [x] Audit action notes and auth 
 - [x] Check import
 - [x] Add home API for Welcome localhost:/ 
 - [ ] Add BackOffice API (get_users, get_notes, get_audit)


## Notes for alembic 
 - `alembic init alembic`
 - Import Base and all Models inside `env.py`
 - `alembic revision --autogenerate -m "Create tables from scratch"`
 - `alembic upgrade head`

