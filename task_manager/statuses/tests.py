from django.test import TestCase
from django.urls import reverse

from ..statuses import consts
from ..statuses.models import Status
from ..tasks.models import Task
from ..users.consts import LOGIN_VIEW
from ..users.models import User


class TestStatuses(TestCase):
    fixtures = [
        'Statuses.json',
        'Users.json',
        'Tasks.json',
        'Labels.json',
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(id=1)
        self.status1 = Status.objects.get(id=1)
        self.task1 = Task.objects.get(id=1)

    def test_statuses_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(consts.LIST_VIEW))
        self.assertEqual(response.status_code, consts.STATUS_OK)
        context_objects = response.context[consts.CONTEXT_OBJECT_NAME]
        db_names = Status.objects.all()
        self.assertQuerysetEqual(context_objects, db_names)

    def test_statuses_list_no_login(self):
        response = self.client.get(reverse(consts.LIST_VIEW))
        self.assertRedirects(response, reverse(LOGIN_VIEW))

    def test_create_status(self):
        self.client.force_login(self.user)
        status = {'name': "status3"}
        response = self.client.post(
            reverse(consts.CREATE_VIEW),
            status,
            follow=True,
        )
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_CREATE_SUCCESS)
        self.assertTrue(Status.objects.filter(name=status['name']).exists())

    def test_change_status(self):
        self.client.force_login(self.user)
        url = reverse(consts.UPDATE_VIEW, args=(self.status1.id,))
        new_status = {'name': 'status4'}
        response = self.client.post(url, new_status, follow=True)
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_UPDATE_SUCCESS)
        changed_status = Status.objects.get(id=self.status1.id)
        self.assertEqual(changed_status.name, 'status4')

    def test_status_with_tasks_delete(self):
        self.client.force_login(self.user)
        url = reverse(consts.DELETE_VIEW, args=(self.status1.id,))
        response = self.client.post(url, follow=True)
        self.assertTrue(Status.objects.filter(id=self.status1.id).exists())
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_DELETE_CONSTRAINT)

    def test_delete_status(self):
        self.client.force_login(self.user)
        self.task1.delete()
        url = reverse(consts.DELETE_VIEW, args=(self.status1.id,))
        response = self.client.post(url, follow=True)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(id=self.status1.id)
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_DELETE_SUCCESS)
