import pytest
from django.contrib.auth.models import User
from task_manager.tests.fixtures.db_fixtures import USERS_TEST


@pytest.fixture
def setup_users(db, django_user_model):
    users = []
    for user in USERS_TEST:
        users.append(django_user_model.objects.create_user(**user))
    return users


@pytest.fixture
def log_user1(client, setup_users):
    credetail = {'username': USERS_TEST[0]['username'],
                 'password': USERS_TEST[0]['password']}
    user = User.objects.get(username=credetail['username'])
    client.login(**credetail)
    return user
