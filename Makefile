.ONESHELL:
SHELL := /bin/bash

.PHONY: run up from_scratch build patch web migrate superuser

up: build web migrate # celery

from_scratch: up superuser

build:
	docker-compose -f docker-compose.yml build

patch:
	docker-compose -f docker-compose.yml build --no-cache

web:
	# if race conditions occur we may need to add a dockerfile entrypoint to wait for postgres
	# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
	docker-compose -f docker-compose.yml up -d web

down:
	docker-compose down
clean: down
	docker-compose down --volumes

# management functions that need to run inside the web container
migrate:
	docker-compose exec web python /app/manage.py makemigrations
	docker-compose exec web python /app/manage.py migrate
superuser:
	# only needed the very first time you initialise a database
	docker-compose exec web python /app/manage.py createsuperuser
