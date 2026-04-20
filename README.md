Oddities
____
эта программа была создана что бы все менеджерирование контентом было в одном месте и не надо было держать рицензии в одном месте а вотчлист в другом, и просто это сделано что бы это было делать удобнее например что бы при добавление вотчлист айтема тебе не надо было вписывать имя режесера, количество серий и эпизодов - программа делает это за тебя, от тебя надо лишь название и начальный год выпуска.
_____
Проект построен на микросервисной логике, упакованной в Docker-контейнеры. Это позволяет изолировать задачи и обеспечивать стабильную работу фоновых процессов

Django + DRF: Ядро системы, API и управление данными

Aiogram: Интерактивный Telegram-бот для пользователей, используется как морда для бэкэнда

Celery + Redis: для удаления аккаунта юзера, где Redis выступает брокером сообщений.

PostgreSQL: база данных.

Docker & Docker Compose: что бы дережировать всеми ими.

Swagger (drf-spectacular): документация к API.

PyJWT : авторизация.
____

технологический стек:
Backend: python 3.14, Django 6.0.2, Django REST Framework 3.16.1

Telegram Bot: Aiogram 3.26.0

Async Tasks: Celery 5.6.2

Cache/Broker: Redis 7.3.0

Database: PostgreSQL

API Docs: Swagger (drf-spectacular 0.29.0)


____


1 - клонируй репозиторий: https://github.com/BugganeHuman/Oddities

2 - создай secret.env файл, на примере example.env

2.1 - если надо скачай docker compose (на пример на линуксе это sudo apt install docker-compose)

3 - в терминале из главной деректории проэкта выполни - docker compose --env-file secret.env up --build

4 - в том же терминале - docker-compose exec web python manage.py migrate

5 - создай супер юзера - docker-compose exec web python manage.py createsuperuser

6 - по адресуу http://localhost:8000/ будут твои эндпоинты,

7 - можешь почитать документацию к API по эндпоинту http://localhost:8000/api/docs/