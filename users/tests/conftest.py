import pytest
from task_manager.tests.fixtures.db_fixtures import USERS_TEST
from task_manager.tests.conftest import (log_user1, setup_users)


@pytest.fixture
def user1_details():
    user1 = USERS_TEST[0].copy()
    user1['password1'] = user1['password']
    user1['password2'] = user1['password']
    return user1
