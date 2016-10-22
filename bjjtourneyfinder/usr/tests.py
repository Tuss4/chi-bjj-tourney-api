from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from unittest.mock import patch
from usrtoken.models import ConfirmationToken
from .views import TourneyEmail


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
        user.is_active = True
        user.save()
        url = reverse('user-login')
        resp = self.client.post(url, self.usr_data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['token'], user.auth_token.key)
        self.assertEqual(resp.data['user']['id'], user.id)
        self.assertEqual(resp.data['user']['email'], self.usr_data['email'])

    def test_confirm_account(self):
        url = reverse('user-register')
        with patch.object(TourneyEmail, 'send_email', return_value=None) as me:
            resp = self.client.post(url, self.usr_data)
        self.assertTrue(me.called)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=self.usr_data['email'])
        self.assertFalse(user.is_active)
        self.assertTrue(ConfirmationToken.objects.filter(user=user).exists())
        ctoken = ConfirmationToken.objects.get(user=user)

        url = reverse('user-confirm', kwargs={'token': ctoken.token})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        user = get_user_model().objects.get(email=self.usr_data['email'])
        self.assertTrue(user.is_active)

    def test_password_reset(self):
        pass
