from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
import itertools

from labels.models import Label
from statuses.models import Status
from tasks import consts
from tasks.models import Task


class TestTasks(TestCase):

    fixtures = [
        "Users.json",
        "Statuses.json",
        "Labels.json",
        "Tasks.json",
    ]

    def setUp(self) -> None:
        # self.label1 = Label.objects.get(pk=1)
        # self.label2 = Label.objects.get(pk=2)
        # self.label3 = Label.objects.get(pk=3)
        # self.label4 = Label.objects.get(pk=4)
        # self.label5 = Label.objects.get(pk=5)

        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
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
        content = response.rendered_content
        lines = content.count('</tr')
        lines_expected = Task.objects.all().count()
        self.assertTrue(lines == lines_expected)
        self.assertTrue(content.find(consts.LIST_TITLE) > 0)
        test_fields = ['name', 'author__first_name', 'author__last_name',
                       'executor__first_name', 'executor__last_name',
                       'status__name']
        for field in test_fields:
            names = Task.objects.values_list(field).all()
            inclusions = list(map(lambda x: content.find(str(*x)) > 0, names))
            self.assertTrue(all(inclusions))

    def test_tasks_list_no_login(self):
        response = self.client.get(reverse(consts.LIST_VIEW))
        self.assertRedirects(response, consts.LOGIN_PAGE)

    def test_create_task(self):
        self.client.force_login(self.user1)
        initial_count = Task.objects.all().count()
        response = self.client.post(
            reverse(consts.CREATE_VIEW),
            self.task,
            follow=True,
        )
        altered_count = Task.objects.all().count()
        self.assertEqual(altered_count, initial_count + 1)
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
        url = reverse(consts.UPDATE_VIEW, args=(self.task1.pk,))
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
        url = reverse(consts.DELETE_VIEW, args=(self.task1.pk,))
        response = self.client.post(url, follow=True)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task1.pk)
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_DELETE_SUCCESS)

    def test_delete_task_not_author(self):
        self.client.force_login(self.user1)
        url = reverse(consts.DELETE_VIEW, args=(self.task2.pk,))
        response = self.client.post(url, follow=True)
        self.assertTrue(Task.objects.filter(pk=self.task2.pk).exists())
        self.assertRedirects(response, reverse(consts.LIST_VIEW))
        self.assertContains(response, consts.MESSAGE_DELETE_CONSTRAINT)

    # def test_filter_self_tasks(self):
    #     """Check filter user's self tasks."""
    #     self.client.force_login(self.user1)
    #     filtered_list = "{0}?self_task=on".format(reverse(TASKS_LIST))
    #     response = self.client.get(filtered_list)
    #     self.assertEqual(response.status_code, STATUS_OK)
    #     self.assertQuerysetEqual(list(response.context[TASKS]), [self.task1])

    # def test_filter_by_status(self):
    #     """Check filter tasks by status."""
    #     self.client.force_login(self.user1)
    #     filtered_list = "{0}?status=2".format(reverse(TASKS_LIST))
    #     response = self.client.get(filtered_list)
    #     self.assertEqual(response.status_code, STATUS_OK)
    #     self.assertQuerysetEqual(list(response.context[TASKS]), [self.task2])

    # def test_filter_by_executor(self):
    #     """Check filter tasks by executor."""
    #     self.client.force_login(self.user1)
    #     filtered_list = "{0}?executor=2".format(reverse(TASKS_LIST))
    #     response = self.client.get(filtered_list)
    #     self.assertEqual(response.status_code, STATUS_OK)
    #     self.assertQuerysetEqual(list(response.context[TASKS]), [self.task1])

    # def test_filter_by_label(self):
    #     """Check filter tasks by label."""
    #     self.client.force_login(self.user1)
    #     self.client.post(reverse(TASKS_CREATE), self.task, follow=True)
    #     created_task = Task.objects.get(name=self.task[NAME])
    #     filtered_list = "{0}?labels=1".format(reverse(TASKS_LIST))
    #     response = self.client.get(filtered_list)
    #     self.assertEqual(response.status_code, STATUS_OK)
    #     self.assertQuerysetEqual(
    #         list(response.context[TASKS]),
    #         [self.task1, created_task],
    #     )
