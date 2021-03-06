from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Country

from country.serializers import CountrySerializer


COUNTRY_URL = reverse('country:country-list')


class PublicCountriesApiTest(TestCase):
    '''Test the publicly available tag api'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''Test that login is required for retrieving list of countries'''
        res = self.client.get(COUNTRY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateClassApiTest(TestCase):
    '''Test the authorised user api tests'''

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'ovansa@gmail.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_countries(self):
        '''Test retrieving countries'''
        Country.objects.create(user=self.user, name="Nigeria")
        Country.objects.create(user=self.user, name="Benin Republic")
        Country.objects.create(user=self.user, name="Ghana")

        res = self.client.get(COUNTRY_URL)

        countries = Country.objects.all().order_by('-name')

        serializer = CountrySerializer(countries, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_country_limited_to_user(self):
        '''Test countries returned are limited to the authenticated user'''
        user2 = get_user_model().objects.create_user(
            'ov@gmail.com',
            'password'
        )

        Country.objects.create(user=user2, name="Cameroon")
        Country.objects.create(user=user2, name="Burkina Faso")

        country1 = Country.objects.create(user=self.user, name="Chad")
        # country2 = Country.objects.create(user=self.user, name="Niger")

        res = self.client.get(COUNTRY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], country1.name)

    def test_create_country_successful(self):
        '''Test creating a new country'''
        payload = {
            'name': 'Nigeria'
        }
        self.client.post(COUNTRY_URL, payload)

        exists = Country.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_country_invalid(self):
        '''Test creating a new country with invalid payload'''
        payload = {'name': ''}
        res = self.client.post(COUNTRY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
