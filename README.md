## Hexlet tests and linter status:
[![Actions Status](https://github.com/Perceptor89/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/Perceptor89/python-project-lvl4/actions)
[![Python CI](https://github.com/Perceptor89/python-project-lvl4/actions/workflows/pyci.yml/badge.svg)](https://github.com/Perceptor89/python-project-lvl4/actions/workflows/pyci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/0fa462337d6ccbb87d30/maintainability)](https://codeclimate.com/github/Perceptor89/python-project-lvl4/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/0fa462337d6ccbb87d30/test_coverage)](https://codeclimate.com/github/Perceptor89/python-project-lvl4/test_coverage)

Task manager is an app which helps you to remember things.

## Example of website:
[Task manager](https://protected-harbor-92063.herokuapp.com "Heroku.com")

## Local installation:
You need to clone repository first:
```bash
git clone https://github.com/Perceptor89/python-project-lvl4
```

The file ".env" should be created in root directory. You should set there local variables:

```
SECRET_KEY='your secret here there'
ROLL_KEY='token from Rollbar error tracker'
# if you want to enter a debug environment
DEBUG=True
```
To install dependencies:

```bash
pip install -r requirements.txt
```

After creation of .env file the migration should be started by two commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

To launch the program:

```bash
python manage.py runserver
```

Usually it starts at address http://127.0.0.1:8000/

The following tools and technologies were used in the project:

| Tool                                                                     | Description                                                                                                           |
|--------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| [django](https://www.djangoproject.com/)                                 | "The web framework for perfectionists with deadlines."                                                   |
| [poetry](https://python-poetry.org/)                                     | "Python dependency management and packaging made easy."                                                             |
| [git](https://git-scm.com)                                               | Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.                                                                       |
| [flake](https://flake8.pycqa.org/en/latest/)                             | "Tool For Style Guide Enforcement."                                                                                 |
| [django unittest](https://docs.djangoproject.com/en/4.0/topics/testing/) | "Django uses the unittest module built into the Python standard library."                                          |
| [i18n](https://docs.djangoproject.com/en/4.0/topics/i18n/)               | "Internationalization and localization."                                                                    |
| [heroku](https://www.heroku.com/)                                        | "Build data-driven apps with fully managed data services."                                                           |
| [rollbar](https://rollbar.com/)                                          | "Proactively discover, predict, and resolve errors in real-time with Rollbar’s continuous code improvement platform." |

## Questions and suggestions:
<andreyfominykh@gmail.com>
