from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse


class UsrTest(APITestCase):

    usr_data = {
        "email": "test@example.com",
        "password": "password1"
    }

    def test_register(self):
        url = reverse('user-register')
        resp = self.client.post(url, self.usr_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Check dupe
        resp = self.client.post(url, self.usr_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_request(self):
        url = reverse('user-register')
        resp = self.client.post(url, {'email': "bruh", "password": "password1"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('user-register')
        resp = self.client.post(url, {"password": "password1"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('user-register')
        resp = self.client.post(url, {'email': "bruh"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('user-register')
        resp = self.client.post(url, {})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        user = get_user_model().objects.create_user(**self.usr_data)
        url = reverse('user-login')
        resp = self.client.post(url, self.usr_data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['token'], user.auth_token.key)
        self.assertEqual(resp.data['user']['id'], user.id)
        self.assertEqual(resp.data['user']['email'], self.usr_data['email'])
