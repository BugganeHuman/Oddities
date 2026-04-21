# Oddities
____
## **About project** 
#### *This program was created so that all content management would be in one place, eliminating the need to keep licenses in one place and a watchlist in another. It was created simply to make it more convenient, for example, so that when adding a watchlist item, you wouldn't have to enter the director's name, the number of series and episodes - the program does it for you; all you need to know is the title and the initial release year.*

### link to tg bot - @Oddities_Diary_Bot

### link to API docs - https://oddities.onrender.com/api/docs/

_____
## **Structure**

### *The project is built on microservice logic packaged in Docker containers. This allows for task isolation and ensures stable operation of background processes.*

- #### Django + DRF: System core, API and data management

- #### Aiogram: An interactive Telegram bot for users, used as a frontend for the backend

- #### Celery + Redis: to delete a user account where Redis acts as a message broker.

- #### PostgreSQL: Database.

- #### Docker & Docker Compose: to manage them all

- #### Swagger (drf-spectacular): Docs for the API.

- #### PyJWT: Auth.
____

## **Technology stack**:

- #### Backend: python 3.14, Django 6.0.2, Django REST Framework 3.16.1

- #### Telegram Bot: Aiogram 3.26.0

- #### Async Tasks: Celery 5.6.2

- #### Cache/Broker: Redis 7.3.0

- #### Database: PostgreSQL

- #### API Docs: Swagger (drf-spectacular 0.29.0)


____
## **Install**

- 1 - clone repository: https://github.com/BugganeHuman/Oddities

- 2 - create secret.env file, in example -  example.env

- 2.1 - if you need, install docker compose (for example - in linux it's  sudo apt install docker-compose)

- 3 - in the terminal from the main directory of the project, run: docker compose --env-file secret.env up --build

- 4 - in the same terminal: docker compose exec web python manage.py migrate

- 5 - create superuser: docker compose exec web python manage.py createsuperuser

- 6 - in url http://localhost:8000/ will have your endpoints

- 7 - you can read the docs for API in this endpoint http://localhost:8000/api/docs/