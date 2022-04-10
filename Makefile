export BROWSER=wslview

heroku-web:
	poetry run heroku open

heroku-local:
	poetry run heroku local

deploy-check:
	poetry run python manage.py check --deploy

requirements:
	poetry export -f requirements.txt --output requirements.txt

run-local:
	poetry run python manage.py runserver
