# python manage.py test core.tests.auth_apis
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationApiTests(APITestCase):

    def test_login(self):
        User.objects.create_user(email='testuser@example.com', password='SecureP@ss123')
        url = reverse('api:auth:jwt:login')
        data = {'email': 'testuser@example.com', 'password': 'SecureP@ss123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)