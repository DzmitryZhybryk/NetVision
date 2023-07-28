## Environment variables:

Для запуска вам понадобится .env файл в корневой директории с переменными окружения

.env file example:

```
DATABASE_URL=postgresql+psycopg://dzmitry_zhybryk:3050132596@postgres/authentication_database
DATABASE_PORT=5432
POSTGRES_USER=dzmitry_zhybryk
POSTGRES_PASSWORD=3050132596
POSTGRES_DB=authentication_database
POSTGRES_HOST=postgres
POSTGRES_HOSTNAME=127.0.0.1
```

## Before start up

Для старта должен быть установлен докер:

- [docker](https://www.docker.com/products/docker-desktop/)

## Start up

### Development mode

Для запуска приложения из директории с docker-compose файлом:

```bash
docker compose -f docker-compose-dev.yml up -d
```

## Swagger documentation

Documentation available on `/api/v1/docs/`
