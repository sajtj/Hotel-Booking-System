# python manage.py test core.tests.users_apis 
from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from django.contrib.auth import get_user_model

from core.users.models import Profile

User = get_user_model()

class RegistrationApiTests(APITestCase):

    def test_register_success(self):
        url = reverse("api:users:register")
        data = {
            'email': 'testuser@example.com',
            'password': 'testuser@example.com1',
            'confirm_password': 'testuser@example.com1',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)

    def test_register_email_already_taken(self):
        User.objects.create(email='testuser@example.com', password='testuser@example.com')
        url = reverse('api:users:register')
        data = {
            'email': 'testuser@example.com',
            'password': 'SecureP@ss123',
            'confirm_password': 'SecureP@ss123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Email Already Taken.', response.data['email'])

    def test_profile_retrieval(self):
        user = User.objects.create_user(email='testuser@example.com', password='SecureP@ss123')
        Profile.objects.create(user=user)
        self.client.force_authenticate(user=user)
        url = reverse('api:users:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)