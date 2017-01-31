from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase


class TestPing(APITestCase):

    def test_ping(self):
        url = reverse("ping-view")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['ping'], "pong")
