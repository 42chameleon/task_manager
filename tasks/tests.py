from django.contrib.auth import get_user_model
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task

User = get_user_model()


class TaskTest(APITestCase):

    def setUp(self):
        self.url_token = reverse('token')
        self.user1 = User.objects.create(username='test user1', password='12345')
        self.user = User.objects.create_user(username='Test_user', password='Test_password')
        response = self.client.post(self.url_token, {'username': 'Test_user', 'password': 'Test_password'},
                                    format='json')
        self.token = response.data['access']
        self.task = Task.objects.create(user=self.user, name='test_task1', description='test_description',
                                        date_end='2004-06-10 00:00')
        self.task1 = Task.objects.create(user=self.user1, name='test_task2', description='test_description2',
                                         date_end='2004-06-10 00:00')

    def test_create_task(self):
        url = reverse('task_create')
        self.client.force_authenticate(self.user, self.token)

        self.data = {
            'name': 'test_task',
            'description': 'test_task_description',
            'date_end': '2004-06-10 00:00'
        }
        response = self.client.post(url, self.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['name'], self.data['name'])
        self.assertEqual(response.data['description'], self.data['description'])

    def test_create_not_auth_user(self):
        self.assertEqual(Task.objects.count(), 2)
        url = reverse('task_create')
        data = {
            'name': 'test_task',
            'description': 'test_task_description',
            'date_end': '2004-06-10 00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(Task.objects.count(), 2)

    def test_get_task(self):
        url = reverse('task_detail', args=(self.task.id,))
        self.client.force_authenticate(self.user, self.token)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['name'], self.task.name)

    def test_get_task_not_auth_user(self):
        url = reverse('task_detail', args=(self.task.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(response.data,
                         {'detail': ErrorDetail(string='Authentication credentials were not provided.',
                                                code='not_authenticated')})

    def test_patch_task(self):
        url = reverse('task_detail', args=(self.task.id,))
        self.client.force_authenticate(self.user, self.token)
        data = {'name': 'name_changed'}
        response = self.client.patch(url, data)
        self.task.refresh_from_db()
        self.assertEqual(data['name'], self.task.name)

    def test_patch_task_not_auth_user(self):
        url = reverse('task_detail', args=(self.task.id,))
        data = {'name': 'name_changed'}
        response = self.client.patch(url, data)
        self.task.refresh_from_db()
        self.assertTrue(self.task.name != data['name'])

    def test_patch_not_owner(self):
        url = reverse('task_detail', args=(self.task.id,))
        self.client.force_authenticate(self.user1)
        data = {'name': 'name_changed'}
        response = self.client.patch(url, data)
        self.task.refresh_from_db()
        self.assertTrue(self.task.name != data['name'])

    def test_delete_task(self):
        url = reverse('task_detail', args=(self.task1.id,))
        self.client.force_authenticate(self.user1, self.token)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_task_not_auth_user(self):
        url = reverse('task_detail', args=(self.task.id,))
        self.client.force_authenticate(self.user1)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(response.data, {
            'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                  code='permission_denied')})
