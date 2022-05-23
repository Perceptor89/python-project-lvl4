from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from labels import consts
from labels.models import Label
from tasks.models import Task
from users.consts import LOGIN_VIEW


class TestLabels(TestCase):
    fixtures = [
        'Labels.json',
        'Tasks.json',
        'Users.json',
        'Statuses.json',
    ]

    def setUp(self) -> None:
        self.user1 = User.objects.get(id=1)
        self.label1 = Label.objects.get(id=1)

    def test_labels_list(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse(consts.LIST_VIEW))
        self.assertEqual(response.status_code, consts.STATUS_OK)
        context_object = response.context[consts.CONTEXT_OBJECT_NAME]
        context_names = context_object.values_list('name').all()
        db_names = Label.objects.values_list('name').all()
        self.assertQuerysetEqual(db_names, context_names)

    def test_labels_list_no_login(self):
        response = self.client.get(reverse(consts.LIST_VIEW))
        self.assertRedirects(response, reverse(LOGIN_VIEW))

    def test_create_label(self):
        self.client.force_login(self.user1)
        test_label = {'name': 'label6'}
        response = self.client.post(
            reverse(consts.CREATE_VIEW), test_label, follow=True
        )
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_CREATE_SUCCESS)
        self.assertTrue(Label.objects.filter(name=test_label['name']).exists())

    def test_change_label(self):
        self.client.force_login(self.user1)
        url = reverse(consts.UPDATE_VIEW, args=(self.label1.id,))
        new_label = {'name': 'changed'}
        response = self.client.post(url, new_label, follow=True)
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_UPDATE_SUCCESS)
        changed_label = Label.objects.get(id=self.label1.id)
        self.assertEqual(changed_label.name, 'changed')

    def test_label_with_tasks_delete(self):
        self.client.force_login(self.user1)
        url = reverse(consts.DELETE_VIEW, args=(self.label1.id,))
        response = self.client.post(url, follow=True)
        self.assertTrue(Label.objects.filter(id=self.label1.id).exists())
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_DELETE_CONSTRAINT)

    def test_delete_label(self):
        Task.objects.all().delete()
        self.client.force_login(self.user1)
        url = reverse(consts.DELETE_VIEW, args=(self.label1.id,))
        response = self.client.post(url, follow=True)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(id=self.label1.id)
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_DELETE_SUCCESS)
