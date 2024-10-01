---
title: CI тесты в Docker c использованием make
draft: false
tags:
  - CI
  - Docker
  - pytest
---
### Библиотеки
Используемые библиотеки для создания тестов:

```toml
[tool.poetry.group.dev.dependencies]
pytest
pytest-asyncio
pytest-mock
httpx
faker
alembic
coverage
```

### docker-compose
Пример `docker-compose.yml `для запуска тестов в Docker контейнерах с подключением к базе данных PostgreSQL и использованием Celery:
```yml
x-postgres-base: &postgres-base
 image: postgres:16
 restart: always
 healthcheck:
  test:
     - CMD-SHELL
     - pg_isready -U postgres
   interval: 10s
   timeout: 5s
   retries: 5

x-app-base: &app-base
  build:
    context: ./backend
  restart: always
  
services:
  postgres-test:
    profiles: ["test"]
    <<: *postgres-base
    env_file: "./backend/.env.test"
    networks:
      - test

  app-test:
    profiles: ["test"]
    <<: *app-base
    command: sh -c "coverage run --source='.' -m pytest -s --rootdir=/app/ --disable-pytest-warnings && coverage html"
    build:
      context: ./backend
      args:
        ENV: test
    env_file: "./backend/.env.test"
    volumes:
      - ./backend/:/app/
    depends_on:
      celery-worker-test:
        condition: service_started
      postgres-test:
        condition: service_healthy
    networks:
      - test

  celery-worker-test:
    profiles: ["test"]
    <<: *app-base
    command: celery -A src.celery_worker:celery worker --loglevel=info
    build:
      context: ./backend
      args:
        ENV: test
    env_file: "./backend/.env.test"
    volumes:
      - ./backend/:/app/
    networks:
      - test
```

### Makefile
Пример `Makefile` для запуска тестов одной командой:

```Makefile
test:
    docker compose -f docker-compose.yml run --rm app-test
    docker compose -f docker-compose.yml --profile test down --volumes
```

### .env.test

Для запуска тестов желательно создать отдельный файл `.env.test` с переменными окружения, куда включить настройки для подключения к тестовой базе данных.

```bash
# Postgres
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres-test
POSTGRES_PORT=5432
```

### workflow.yml

При необходимости, можно [[sed - изменение секретов .env файла|заменить переменные в .env.test]] для корректного запуска тестов в GitHub Actions.

```yml
  backend_tests:
    name: Backend Tests
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4
      - name: Tests in Docker Container
        run: |
          make test
```

----
📂 [[GitHub Actions]]

Последнее изменение: 01.10.2024 16:18