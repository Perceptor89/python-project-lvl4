from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from statuses import consts
from .models import Status


class TestStatuses(TestCase):

    fixtures = [
        "Statuses.json", 
        "Users.json", 
        # "tasks.json", 
        # "labels.json"
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        # self.task1 = Task.objects.get(pk=1)

    def test_statuses_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(consts.LIST_VIEW))
        self.assertEqual(response.status_code, consts.STATUS_OK)
        db_names = Status.objects.values_list('name').all()
        context_names = [
            (x.name,) for x in response.context[consts.STATUS_MODEL_VAR]
        ]
        self.assertQuerysetEqual(db_names, context_names)

    def test_statuses_list_no_login(self):
        response = self.client.get(reverse(consts.LIST_VIEW))
        self.assertRedirects(response, consts.LOGIN_PAGE)

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
        created_status = Status.objects.get(name=status['name'])
        self.assertEquals(created_status.name, "status3")

    def test_change_status(self):
        self.client.force_login(self.user)
        url = reverse(consts.UPDATE_VIEW, args=(self.status1.pk,))
        new_status = {'name': "status4"}
        response = self.client.post(url, new_status, follow=True)
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_UPDATE_SUCCESS)
        self.assertEqual(Status.objects.get(pk=self.status1.id), self.status1)

    # def test_status_with_tasks_delete(self):
    #     self.client.force_login(self.user)
    #     url = reverse(STATUSES_DELETE, args=(self.status1.pk,))
    #     response = self.client.post(url, follow=True)
    #     self.assertTrue(Status.objects.filter(pk=self.status1.id).exists())
    #     self.assertRedirects(response, STATUSES_TEST)
    #     self.assertContains(response, STATUS_IN_USE)

    def test_delete_status(self):
        self.client.force_login(self.user)
        # self.task1.delete()
        url = reverse(consts.DELETE_VIEW, args=(self.status1.pk,))
        response = self.client.post(url, follow=True)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(pk=self.status1.pk)
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_DELETE_SUCCESS)
