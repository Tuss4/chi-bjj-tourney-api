from datetime import date, timedelta
from copy import copy
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Event, TOURNAMENT
from usrprofile.models import Profile


class EventTest(APITestCase):

    res_obj = {
        "name": "Super Legit BJJ Tournament",
        "website": "http://superlegitbjjtournament.org",
        "early_registration_date": date.today() - timedelta(weeks=8),
        "registration_date": date.today() + timedelta(weeks=12),
        "early_price": "89.99",
        "price": "99.99",
        "event_type": TOURNAMENT
    }

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            "luke.cage@harlem.io", "password1")
        self.client.force_authenticate(user=self.user)

    def list_route(self):
        return reverse('event-list')

    def detail_route(self, pk):
        return reverse('event-detail', kwargs={'pk': pk})

    def test_create(self):
        resp = self.client.post(self.list_route(), self.res_obj)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        result = resp.data
        self.assertEqual(result['name'], self.res_obj['name'])
        self.assertEqual(result['website'], self.res_obj['website'])
        self.assertEqual(
            result['early_registration_date'], self.res_obj['early_registration_date'].isoformat())
        self.assertEqual(result['registration_date'], self.res_obj['registration_date'].isoformat())
        self.assertEqual(result['price'], self.res_obj['price'])
        self.assertEqual(result['early_price'], self.res_obj['early_price'])
        self.assertEqual(result['event_type'], TOURNAMENT)

    def test_list(self):
        resp = self.client.post(self.list_route(), self.res_obj)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        obj_id = resp.data['id']

        resp = self.client.get(self.list_route())
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 0)
        self.assertFalse(resp.data['results'])

        obj = Event.objects.get(pk=obj_id)
        obj.approved = True
        obj.save()

        resp = self.client.get(self.list_route())
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.data['results'][0]['id'], obj_id)

        self.client.force_authenticate(user=None)
        resp = self.client.get(self.list_route())
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_retrieve(self):
        resp = self.client.post(self.list_route(), self.res_obj)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        obj_id = resp.data['id']

        resp = self.client.get(self.detail_route(obj_id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        result = resp.data
        self.assertEqual(result['name'], self.res_obj['name'])
        self.assertEqual(result['website'], self.res_obj['website'])
        self.assertEqual(
            result['early_registration_date'], self.res_obj['early_registration_date'].isoformat())
        self.assertEqual(result['registration_date'], self.res_obj['registration_date'].isoformat())
        self.assertEqual(result['price'], self.res_obj['price'])
        self.assertEqual(result['early_price'], self.res_obj['early_price'])
        self.assertEqual(result['event_type'], TOURNAMENT)

    def test_update(self):
        resp = self.client.post(self.list_route(), self.res_obj)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        obj_id = resp.data['id']

        o = copy(self.res_obj)
        o['price'] = "109.99"

        resp = self.client.put(self.detail_route(obj_id), o)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['price'], o['price'])

    def test_partial_update(self):
        resp = self.client.post(self.list_route(), self.res_obj)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        obj_id = resp.data['id']

        resp = self.client.patch(self.detail_route(obj_id), {'price': "109.99"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['price'], "109.99")

    def test_delete(self):
        resp = self.client.post(self.list_route(), self.res_obj)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        obj_id = resp.data['id']

        resp = self.client.delete(self.detail_route(obj_id))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)


class ModerateEvent(APITestCase):

    res_obj = {
        "name": "Super Legit BJJ Tournament",
        "website": "http://superlegitbjjtournament.org",
        "early_registration_date": date.today() - timedelta(weeks=8),
        "registration_date": date.today() + timedelta(weeks=12),
        "early_price": "89.99",
        "price": "99.99",
        "event_type": TOURNAMENT
    }

    res_obj_2 = {
        "name": "Fight Pro Grappling League Submission Championships",
        "website": "http://fpglschamps.org",
        "early_registration_date": date.today() - timedelta(weeks=8),
        "registration_date": date.today() + timedelta(weeks=18),
        "early_price": "79.99",
        "price": "109.99",
        "event_type": TOURNAMENT
    }

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            "luke.cage@harlem.io", "password1")
        Profile.objects.create(user=self.user, display_name="PowerMan")
        self.reg = get_user_model().objects.create_user(
            "misty.knight@harlem.io", "password1")
        Profile.objects.create(user=self.reg, display_name="MistyKnight")
        self.client.force_authenticate(user=self.user)

    def list_route(self):
        return reverse('moderate-event-list')

    def detail_route(self, pk):
        return reverse('moderate-event-detail', kwargs={'pk': pk})

    def test_unauthorized(self):
        self.client.force_authenticate(user=None)
        resp = self.client.get(self.list_route())
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_forbidden(self):
        self.client.force_authenticate(user=self.reg)
        resp = self.client.get(self.list_route())
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderate_events(self):
        Event.objects.create(
            **self.res_obj_2, approved=True, author=self.user)
        self.client.force_authenticate(user=self.reg)
        # Regular creates event
        url = reverse('event-list')
        # Doesn't show up in event list
        resp = self.client.post(url, self.res_obj)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        event_id = resp.data['id']
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)
        # Moderator approves it
        self.client.force_authenticate(user=self.user)
        resp = self.client.get(self.list_route())
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)
        resp = self.client.patch(self.detail_route(event_id), {'approved': True})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['approved'])
        # Shows up in event list
        self.client.force_authenticate(user=self.reg)
        url = reverse('event-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 2)
