from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()


class TokenLoginTest(TestCase):
    def setUp(self):
        self.apicilent = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@test.org'
        )
        self.url = reverse('userprofile:login')

    def test_username_login(self):
        data = {
            'username': 'admin',
            'password': 'admin',
        }
        response = self.apicilent.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(response.data['token'],
                         Token.objects.get(user=self.user).__str__())

    def test_email_login(self):
        data = {
            'username': 'admin@test.org',
            'password': 'admin',
        }
        response = self.apicilent.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            'username': 'admin@test.or',
            'password': 'admin',
        }
        response = self.apicilent.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TokenLogoutTest(TestCase):
    def setUp(self):
        self.apicilent = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@test.org'
        )
        self.login_url = reverse('userprofile:login')
        self.logout_url = reverse('userprofile:logout')

    def test_logout(self):
        data = {
            'username': 'admin',
            'password': 'admin',
        }
        self.apicilent.post(self.login_url, data=data, format='json')

        response = self.apicilent.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.apicilent.login(username='admin', password='admin')
        response = self.apicilent.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user))


class UserProfileDetailViewTest(TestCase):
    def setUp(self):
        self.apiclient = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@test.org'
        )
        self.url = reverse('userprofile:profile')

    def test_get_user_profile(self):
        response = self.apiclient.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.apiclient.login(username='admin', password='admin')
        response = self.apiclient.get(self.url)

    def test_update_user_password(self):
        data = {
            'username': 'admin',
            'password': 'testadmin',
            'email': 'admin@test.org',
        }
        response = self.apiclient.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.apiclient.login(username='admin', password='admin')
        response = self.apiclient.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        is_login = self.apiclient.login(username='admin', password='testadmin')
        self.assertTrue(is_login)

    def test_update_user_username_and_email(self):
        data = {
            'username': 'testadmin',
            'email': 'admin@test.or',
        }
        response = self.apiclient.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.apiclient.login(username='admin', password='admin')
        response = self.apiclient.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testadmin')
        self.assertEqual(self.user.email, 'admin@test.or')


class UserProfileCreateViewTest(TestCase):
    def setUp(self):
        self.apiclient = APIClient()
        self.url = reverse('userprofile:register')

    def test_create_user(self):
        data = {
            'username': 'admin',
            'password': 'admin',
            'email': 'admin@test.org',
        }
        response = self.apiclient.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(id=response.data['id'])
        self.assertEqual(user.username, 'admin')
