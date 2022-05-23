MANAGE := poetry run python manage.py
export BROWSER=wslview

heroku-web:
	poetry run heroku open

heroku-local:
	poetry run heroku local

deploy-check:
	@$(MANAGE) check --deploy

requirements:
	poetry export -f requirements.txt --output requirements.txt

run-local:
	@$(MANAGE) runserver

.PHONY: makemigrations
makemigrations:
	@$(MANAGE) makemigrations

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus

makemessages:
	django-admin makemessages -a

compilemessages:
	django-admin compilemessages

.PHONY: lint
lint:
	@poetry run flake8 task_manager

.PHONY: test
test:
	@$(MANAGE) test
