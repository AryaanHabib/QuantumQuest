# tasks/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class TaskAPITests(APITestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Test Task", description="Test Description")

    def test_list_tasks(self):
        url = reverse('task-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_create_task(self):
        url = reverse('task-list-create')
        data = {"title": "New Task", "description": "New Description", "is_completed": False}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_update_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {"title": "Updated Task", "description": "Updated Description", "is_completed": True}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    def test_delete_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
