from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker

from django.urls import reverse

from accounts.models import User
from accounts.tests.factories import UserFactory


fake = Faker()


class UserAuthTests(APITestCase):
    """
    Test suite for user registration, login, profile retrieval, and logout.
    """

    def setUp(self):
        """
        Initialize test user and common URLs.
        """
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.me_url = reverse('me')
        self.refresh_url = reverse('token_refresh')

        self.password = "SecurePass123"
        self.user = UserFactory(password=self.password)

        # Get tokens via login
        login_response = self.client.post(self.login_url, {
            "email": self.user.email,
            "password": self.password
        })

        self.access_token = login_response.data["access"]
        self.refresh_token = login_response.data["refresh"]

    def test_register_user(self):
        """
        Test that a user can register with valid data.
        """
        data = {
            "name": fake.name(),
            "email": fake.unique.email(),
            "password": "MyNewPass123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_login_user(self):
        """
        Test that an existing user can log in and receive tokens.
        """
        response = self.client.post(self.login_url, {
            "email": self.user.email,
            "password": self.password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_get_user_profile(self):
        """
        Test retrieving the current user's profile using a valid access token.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["name"], self.user.name)

    def test_successful_logout(self):
        """
        Test logout with a valid refresh token.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post(self.logout_url, {"refresh": self.refresh_token})

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data["detail"], "Successfully logged out.")

    def test_blacklisted_token_cannot_be_refreshed(self):
        """
        Test that a blacklisted refresh token cannot be used to get a new access token.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.client.post(self.logout_url, {"refresh": self.refresh_token})

        # Try using the same refresh token
        response = self.client.post(self.refresh_url, {"refresh": self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Token is blacklisted", str(response.data))

    def test_logout_with_invalid_token(self):
        """
        Test logout fails with an invalid refresh token.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post(self.logout_url, {"refresh": "invalid_token_here"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Token is invalid", str(response.data))

    def test_logout_unauthenticated(self):
        """
        Test logout fails if user is not authenticated (missing access token).
        """
        response = self.client.post(self.logout_url, {"refresh": self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
