from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import State

from country.serializers import StateSerializer


STATE_URL = reverse('country:state-list')


class PublicStateApiTest(TestCase):
    '''Test the publicly available state API'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''Test that login is required to access the endpoints'''
        res = self.client.get(STATE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStateApiTest(TestCase):
    '''Test the private state API'''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'ovansa@gmail.com', 'password'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_states_list(self):
        '''Test retrieving a list of states'''
        State.objects.create(user=self.user, name='Lagos')
        State.objects.create(user=self.user, name='Kano')

        res = self.client.get(STATE_URL)

        states = State.objects.all().order_by('-name')
        serializer = StateSerializer(states, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_states_limited_to_user(self):
        '''Test states are limited to authenticated user'''
        user2 = get_user_model().objects.create_user(
            'ov@gmail.com', 'password'
        )

        State.objects.create(user=user2, name='Oyo')
        state = State.objects.create(user=self.user, name='Kwara')

        res = self.client.get(STATE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], state.name)
