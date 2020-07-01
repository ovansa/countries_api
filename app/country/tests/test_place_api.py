from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Place, Country, State

from country.serializers import PlaceSerializer, PlaceDetailSerializer


PLACE_URL = reverse('country:place-list')


def detail_url(place_id):
    '''Return place detail url'''
    return reverse('country:place-detail', args=[place_id])


def sample_country(user, name='Nigeria'):
    '''Create and return a sample country'''
    return Country.objects.create(user=user, name=name)


def sample_state(user, name='Lagos'):
    '''Create and return sample state'''
    return State.objects.create(user=user, name=name)


def sample_place(user, **params):
    '''Create and return a sample place'''
    defaults = {
        'name': 'Ipaja'
    }
    defaults.update(params)

    return Place.objects.create(user=user, **defaults)


class PublicPlaceApiTest(TestCase):
    '''Test unauthenticated place API acess'''

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        '''Test that authentication is required'''
        res = self.client.get(PLACE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    '''Test authenticated place API'''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'ovan@gmail.com', 'password'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_places(self):
        '''Test retrieving a list of places'''
        sample_place(user=self.user)
        sample_place(user=self.user)

        res = self.client.get(PLACE_URL)

        places = Place.objects.all().order_by('-id')
        serializer = PlaceSerializer(places, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_places_limited_to_user(self):
        '''Test retrieving places for user'''
        user2 = get_user_model().objects.create_user(
            'ovansa@gmail.com', 'password'
        )

        sample_place(user=user2)
        sample_place(user=self.user)

        res = self.client.get(PLACE_URL)

        places = Place.objects.filter(user=self.user)
        serializer = PlaceSerializer(places, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_place_detail(self):
        '''Test viewing a place detail'''
        place = sample_place(user=self.user)
        place.country.add(sample_country(user=self.user))
        place.state.add(sample_state(user=self.user))

        url = detail_url(place.id)
        res = self.client.get(url)

        serializer = PlaceDetailSerializer(place)

        self.assertEqual(res.data, serializer.data)
