from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from users import consts
from tasks.models import Task


class TestUsers(TestCase):
    fixtures = [
        'Users.json',
        'Statuses.json',
        'Labels.json',
        'Tasks.json',
    ]

    def setUp(self) -> None:
        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)

    def test_users_list(self):
        response = self.client.get(reverse(consts.LIST_VIEW))
        self.assertEqual(response.status_code, consts.STATUS_OK)
        users_list = response.context[consts.CONTEXT_OBJECT_NAME]
        db_users = User.objects.all()
        self.assertEqual(users_list.count(), db_users.count())
        self.assertQuerysetEqual(
            users_list.values_list('first_name', 'last_name'),
            db_users.values_list('first_name', 'last_name'),
            ordered=False,
        )

    def test_user_create(self):
        url = reverse(consts.CREATE_VIEW)
        new_user = {
            'username': "Testuser",
            'first_name': "Firstname",
            'last_name': "Lastname",
            'password1': "L8d9test66",
            'password2': "L8d9test66",
        }
        response = self.client.post(url, new_user, follow=True)
        self.assertRedirects(response, reverse(consts.LOGIN_VIEW))
        self.assertContains(response, consts.MESSAGE_CREATE_SUCCESS)
        created_user = User.objects.get(username=new_user['username'])
        login_status = self.client.login(
            username=new_user['username'],
            password=new_user['password1'],
        )
        self.assertTrue(login_status)

    def test_user_update(self):
        self.client.force_login(self.user1)
        url = reverse(consts.UPDATE_VIEW, args=(self.user1.id,))
        new_data = {
            'username': self.user1.username,
            'first_name': self.user1.first_name,
            'last_name': self.user1.last_name,
            'password1': "O5D2c9l35874",
            'password2': "O5D2c9l35874",
        }
        response = self.client.post(url, new_data, follow=True)
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_UPDATE_SUCCESS)
        changed_user = User.objects.get(username=self.user1.username)
        self.assertTrue(changed_user.check_password("O5D2c9l35874"))

    def test_user_delete(self):
        Task.objects.all().delete()
        self.client.force_login(self.user1)
        url = reverse(consts.DELETE_VIEW, args=(self.user1.id,))
        response = self.client.post(url, follow=True)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user1.id)
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_DELETE_SUCCESS)
