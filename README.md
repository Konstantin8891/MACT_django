# MACT_django

## Парсинг музейных сайтов

### Стек

Django

DRF

PostgreSQL

Aiohttp

### Инструкции по запуску проекта

git clone git@github.com:Konstantin8891/MACT_django.git

cd infra

docker-compose up --build

docker exec -it infra_back_1 bash

python manage.py shell < fullfill_db_correct.py

exit

### Поисковый запрос 

GET http://localhost:8000/?q={текст_запроса}

### env файл (пример)

SECRET_KEY=some_key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
