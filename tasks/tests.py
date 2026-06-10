from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()


class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_task_creation_with_defaults(self):
        task = Task.objects.create(title='テスト', created_by=self.user)
        self.assertEqual(task.status, 'todo')
        self.assertIsNone(task.due_date)

    def test_task_str(self):
        task = Task.objects.create(title='会議準備', created_by=self.user)
        self.assertEqual(str(task), '会議準備')

    def test_status_display(self):
        task = Task.objects.create(title='テスト', created_by=self.user, status='in_progress')
        self.assertEqual(task.get_status_display(), '進行中')

    def test_task_update_status(self):
        task = Task.objects.create(title='テスト', created_by=self.user)
        task.status = 'done'
        task.save()
        task.refresh_from_db()
        self.assertEqual(task.status, 'done')


class TaskViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_task_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks:task_list'))
        self.assertRedirects(response, '/accounts/login/?next=/tasks/')

    def test_task_list_shows_own_tasks(self):
        Task.objects.create(title='自分のタスク', created_by=self.user)
        other_user = User.objects.create_user(username='other', password='pass')
        Task.objects.create(title='他人のタスク', created_by=other_user)

        response = self.client.get(reverse('tasks:task_list'))
        self.assertContains(response, '自分のタスク')
        self.assertNotContains(response, '他人のタスク')

    def test_task_create(self):
        response = self.client.post(reverse('tasks:task_create'), {
            'title': '新しいタスク',
            'status': 'todo',
        })
        self.assertEqual(response.status_code, 302)   # リダイレクトされる
        self.assertTrue(Task.objects.filter(title='新しいタスク').exists())
