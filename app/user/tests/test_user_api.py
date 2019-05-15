from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
# Make requests to the API and check the response
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def get_dummy_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user public apu"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload"""
        payload = {
            'email': 'user@gmail.com',
            'password': 'password123',
            'name': 'User1'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'user@gmail.com',
            'password': 'password123',
            'name': 'User1'
        }

        get_dummy_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_length_validation(self):
        """Tests the password is long enough"""
        payload = {
            'email': 'user@gmail.com',
            'password': 'pa',
            'name': 'User1'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test if the token is created for the user"""
        payload = {
            'email': 'user@gmail.com',
            'password': 'pa',
            'name': 'User1'
        }
        get_dummy_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Token is not created if invalid credentials are given"""
        get_dummy_user(email='user@gmail.com',
                       password='password123')
        payload = {
            'email': 'user@gmail.com',
            'password': 'wrongPass'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Token is not created if the user doesn't exist"""
        payload = {
            'email': 'user@gmail.com',
            'password': 'wrongPass'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {
            'email': 'user@gmail.com',
            'password': 'wrongPass'
        })

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
