from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='ovansa@gmail.com', password='password'):
    '''Create a sample user'''
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        '''Test creating a new user with an email is successful'''
        email = 'ovansa@gmail.com'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_email_and_no_password_successful(self):
        '''Test creating a new user with email and no password'''
        email = 'ovansa@gmail.com'
        user = get_user_model().objects.create_user(
            email=email
        )
        self.assertTrue(user.email, email)

    def test_new_user_email_normalized(self):
        '''Test the email for a new user is normalized i.e.
        converted to lowercase'''
        email = 'ovansa@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        '''Test creating user with no email raises error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_superuser(self):
        '''Test creating a new superuser'''
        user = get_user_model().objects.create_superuser(
            'ovansa@gmail.com',
            'password'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        '''Test the tag string representation'''
        tag = models.Country.objects.create(
            user=sample_user(),
            name='Africa'
        )

        self.assertEqual(str(tag), tag.name)
