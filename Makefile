MANAGE := poetry run python manage.py
export BROWSER=wslview

web:
	poetry run heroku open

check:
	@$(MANAGE) check --deploy

requirements:
	poetry export -f requirements.txt --output requirements.txt

run:
	@$(MANAGE) runserver

migrate:
	@$(MANAGE) makemigrations
	@$(MANAGE) migrate

shell:
	@$(MANAGE) shell_plus

locale:
	django-admin makemessages -a

translate:
	django-admin compilemessages

lint:
	poetry run flake8 task_manager/ labels/ statuses/ users/ tasks/

test:
	@$(MANAGE) test

coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml
	poetry run coverage report

.PHONY: run test lint translate check web