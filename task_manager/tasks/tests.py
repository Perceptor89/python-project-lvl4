from django.test import TestCase
from django.urls import reverse
import itertools

from ..users.consts import LOGIN_VIEW
from ..users.models import User
from ..tasks import consts
from ..tasks.models import Task


class TestTasks(TestCase):
    fixtures = [
        'Users.json',
        'Statuses.json',
        'Labels.json',
        'Tasks.json',
    ]

    def setUp(self):
        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)

        self.task1 = Task.objects.get(id=1)
        self.task2 = Task.objects.get(id=2)
        self.task = {
            'name': "task3",
            'description': "description3",
            'status': 1,
            'executor': 2,
            'labels': [
                1,
                2
            ],
        }

    def test_tasks_list(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse(consts.LIST_VIEW))
        self.assertEqual(response.status_code, consts.STATUS_OK)
        self.assertContains(response, consts.LIST_TITLE)
        content_tasks = response.context[consts.CONTEXT_OBJECT_NAME]
        db_tasks = Task.objects.all()
        self.assertQuerysetEqual(content_tasks, db_tasks)

    def test_tasks_list_no_login(self):
        response = self.client.get(reverse(consts.LIST_VIEW))
        self.assertRedirects(response, reverse(LOGIN_VIEW))

    def test_create_task(self):
        self.client.force_login(self.user1)
        count_before = Task.objects.all().count()
        response = self.client.post(
            reverse(consts.CREATE_VIEW),
            self.task,
            follow=True,
        )
        count_after = Task.objects.all().count()
        self.assertEqual(count_after, count_before + 1)
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_CREATE_SUCCESS)
        created_task = Task.objects.get(name=self.task['name'])
        self.assertEqual(created_task.description, self.task['description'])
        self.assertEqual(created_task.executor.id, self.task['executor'])
        self.assertEqual(created_task.author.id, self.user1.id)
        self.assertEqual(created_task.status.id, self.task['status'])
        assigned_labels = list(
            itertools.chain(*created_task.labels.values_list('id'))
        )
        self.assertEqual(assigned_labels, self.task['labels'])

    def test_change_task(self):
        self.client.force_login(self.user1)
        count_before = Task.objects.all().count()
        url = reverse(consts.UPDATE_VIEW, args=(self.task1.id,))
        response = self.client.post(url, self.task, follow=True)
        count_after = Task.objects.all().count()
        self.assertEqual(count_before, count_after)
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_UPDATE_SUCCESS)
        updated_task = Task.objects.get(name=self.task['name'])
        self.assertEqual(updated_task.description, self.task['description'])
        self.assertEqual(updated_task.executor.id, self.task['executor'])
        self.assertEqual(updated_task.author.id, self.user1.id)
        self.assertEqual(updated_task.status.id, self.task['status'])
        assigned_labels = list(
            itertools.chain(*updated_task.labels.values_list('id'))
        )
        self.assertEqual(assigned_labels, self.task['labels'])

    def test_delete_task(self):
        self.client.force_login(self.user1)
        url = reverse(consts.DELETE_VIEW, args=(self.task1.id,))
        response = self.client.post(url, follow=True)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task1.id)
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_DELETE_SUCCESS)

    def test_delete_task_not_author(self):
        self.client.force_login(self.user1)
        url = reverse(consts.DELETE_VIEW, args=(self.task2.id,))
        response = self.client.post(url, follow=True)
        self.assertTrue(Task.objects.filter(id=self.task2.id).exists())
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_DELETE_CONSTRAINT)

    def test_filter_self_tasks(self):
        self.client.force_login(self.user1)
        filtered_list = "{0}?self_task=on".format(reverse(consts.LIST_VIEW))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, consts.STATUS_OK)
        listed_tasks = response.context[consts.CONTEXT_OBJECT_NAME]
        db_filtered_tasks = Task.objects.filter(id=self.user1.id)
        self.assertQuerysetEqual(
            listed_tasks,
            db_filtered_tasks,
        )

    def test_filter_by_status(self):
        test_status_id = 2
        self.client.force_login(self.user1)
        filtered_list = "{0}?status={1}".format(
            reverse(consts.LIST_VIEW), test_status_id
        )
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, consts.STATUS_OK)
        listed_tasks = response.context[consts.CONTEXT_OBJECT_NAME]
        for task in listed_tasks:
            self.assertEqual(task.status_id, test_status_id)

    def test_filter_by_executor(self):
        test_executor_id = 2
        self.client.force_login(self.user1)
        filtered_list = "{0}?executor={1}".format(
            reverse(consts.LIST_VIEW), test_executor_id
        )
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, consts.STATUS_OK)
        listed_tasks = response.context[consts.CONTEXT_OBJECT_NAME]
        for task in listed_tasks:
            self.assertEqual(task.executor_id, test_executor_id)

    def test_filter_by_label(self):
        test_label_id = 1
        self.client.force_login(self.user1)
        self.client.post(reverse(consts.CREATE_VIEW), self.task, follow=True)
        filtered_list = "{0}?labels={1}".format(
            reverse(consts.LIST_VIEW), test_label_id
        )
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, consts.STATUS_OK)
        for task in response.context[consts.CONTEXT_OBJECT_NAME]:
            db_task = Task.objects.get(id=task.id)
            assigned_labels = list(
                itertools.chain(*db_task.labels.values_list('id'))
            )
            self.assertIn(test_label_id, assigned_labels)
