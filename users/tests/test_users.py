import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from users.consts import CREATE_VIEW, UPDATE_VIEW, LIST_VIEW, DELETE_VIEW


NEW_USER = {
    "first_name": "Malika",
    "last_name": "Hodkiewicz",
    "full_name": "Malika Hodkiewicz",
    "username": "malika-hodkiewicz",
    "password1": "8RvGr5wWTu",
    "password2": "8RvGr5wWTu"
}


@pytest.mark.django_db
def test_register_post_normal(client):
    response = client.post(reverse(CREATE_VIEW), NEW_USER)
    created_user = User.objects.get(username=NEW_USER['username'])
    assert created_user
    assert created_user.get_full_name() == NEW_USER['full_name']
    assert response.status_code == 302
    expected_url = reverse("login")
    assert response.url == expected_url
    assert not response.wsgi_request.user.is_authenticated
    login_status = client.login(
        username=NEW_USER['username'],
        password=NEW_USER['password1'])
    assert login_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'update_field', ['first_name', 'last_name', 'username', 'password'])
def test_update_self(client, setup_users, update_field,
                     log_user1, user1_details):
    updated_user_data = user1_details.copy()
    updated_user_data[update_field] = updated_user_data[update_field] + 'tests'
    updated_user_data['password1'] = updated_user_data['password']
    updated_user_data['password2'] = updated_user_data['password']
    response = client.post(reverse(UPDATE_VIEW, kwargs={'pk': log_user1.id}),
                           updated_user_data)
    user_db = User.objects.get(id=log_user1.id)
    assert not response.wsgi_request.user.is_authenticated
    assert response.url == reverse(LIST_VIEW)
    assert user_db.username == updated_user_data['username']
    assert user_db.first_name == updated_user_data['first_name']
    assert user_db.last_name == updated_user_data['last_name']
    credetails = {'username': updated_user_data['username'],
                  'password': updated_user_data['password']}
    login_status = client.login(**credetails)
    assert login_status


@pytest.mark.django_db
def test_delete_self(client, setup_users, log_user1):
    response = client.post(reverse(DELETE_VIEW, kwargs={'pk': log_user1.id}))
    with pytest.raises(Exception) as e:
        User.objects.get(username=log_user1.username)
    assert e.match('User matching query does not exist')
    assert User.objects.all().count() == len(setup_users) - 1
    assert response.status_code == 302
    assert response.url == reverse(LIST_VIEW)
