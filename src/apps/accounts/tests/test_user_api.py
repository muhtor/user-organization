from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

REGISTER_USER_URL = reverse("accounts:register")
DETAIL_USER_URL = reverse("accounts:me", args=(1, ))
TOKEN_CREATE_URL = reverse("token_create")
TOKEN_REFRESH_URL = reverse("token_refresh")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            "email": "user@example.com",
            "password": "12345678i",
            "password2": "12345678i",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+70011234567"
        }
        res = self.client.post(REGISTER_USER_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=res.data['results']['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {
            "email": "user@example.com",
            "password": "12345678i",
            "password2": "12345678i",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+70011234567"
        }
        create_user(**payload)

        # creating user with API using same credentials
        res = self.client.post(REGISTER_USER_URL, payload, format="json")
        self.assertIn("errors", res.data)
        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 8 characters. This is default 8 character limit by Django."""
        payload = {
            "email": "user@example.com",
            "password": "pw",
            "password2": "pw",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+70011234567"
        }
        res = self.client.post(REGISTER_USER_URL, payload, format="json")
        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_password_not_equal(self):
        """Test that the password must be equal."""
        payload = {
            "email": "user@example.com",
            "password": "pw",
            "password2": "Pw1",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+70011234567"
        }
        res = self.client.post(REGISTER_USER_URL, payload, format="json")
        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {"email": "test@admin.com", "password": "testpass"}
        create_user(**payload)

        res = self.client.post(TOKEN_CREATE_URL, payload, format="json")
        self.assertIn("access", res.data['results'])
        self.assertIn("refresh", res.data['results'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email="test@admin.com", password="testpass")
        payload = {"email": "test@admin.com", "password": "testfail"}
        res = self.client.post(TOKEN_CREATE_URL, payload, format="json")
        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {"email": "test@admin.com", "password": "testpass"}
        res = self.client.post(TOKEN_CREATE_URL, payload, format="json")
        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_missing_fields(self):
        """Test that email and password are required"""
        payload = {"email": "test", "password": ""}
        res = self.client.post(TOKEN_CREATE_URL, payload, format="json")
        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        payload = {
            "email": "user@example.com",
            "password": "12345678i",
            "password2": "12345678i",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+70011234567"
        }

        self.user = create_user(**payload)
        self.client = APIClient()
        res = self.client.post(TOKEN_CREATE_URL, {"email": "user@example.com", "password": "12345678i"}, format="json")
        self.access_token = res.data['results']["access"]
        self.refresh_token = res.data['results']["refresh"]

    def test_retrieve_profile_success(self):
        """Test profile info for logged in user"""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(DETAIL_USER_URL)

        self.assertIn("email", res.data['results'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)

    def test_retrieve_profile_logout(self):
        """Test profile cannot be seen if not logged out"""
        res = self.client.get(DETAIL_USER_URL)
        self.assertNotIn("email", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_inactive_user_api_simplejwt(self):
        """Test that inactive user is not able to get an access token"""
        payload = {
            "email": "user@example.com",
            "password": "12345678i",
            "password2": "12345678i",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+70011234567"
        }
        self.user.is_active = False
        self.user.save()
        res = self.client.post(TOKEN_CREATE_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_profile_fail_using_jwt(self):
        """Test profile info using incorrect jwt token"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "abc")
        res = self.client.get(DETAIL_USER_URL)
        self.assertNotIn("email", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_profile_success_using_jwt(self):
        """Test profile info using correct jwt token"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        res = self.client.get(DETAIL_USER_URL)
        self.assertIn("email", res.data['results'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_using_refresh_token_success(self):
        """Test that creating access token using correct refresh token succeeds"""
        res = self.client.post(TOKEN_REFRESH_URL, {"refresh": self.refresh_token}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # quick test new access token works
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + res.data['results']["access"])
        res = self.client.get(DETAIL_USER_URL)
        self.assertIn("email", res.data['results'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
