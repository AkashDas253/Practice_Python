from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from unittest.mock import patch

User = get_user_model()

class AccountTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('user-register-api')
        self.login_url = reverse('api_token_auth')
        self.me_url = reverse('user-me-api')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123'
        }

    # REGISTRATION TESTS

    def test_registration_success(self):
        """Test successful registration returns user data and token."""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertTrue(Token.objects.filter(user__username='testuser').exists())

    def test_registration_duplicate_username(self):
        """Test that registering an existing username fails."""
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # LOGIN / TOKEN TESTS

    def test_login_success(self):
        """Test that valid credentials return a token."""
        User.objects.create_user(username='loginuser', password='password123')
        data = {'username': 'loginuser', 'password': 'password123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        """Test that wrong password returns 400."""
        User.objects.create_user(username='loginuser', password='password123')
        data = {'username': 'loginuser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # PROFILE / AUTHENTICATION TESTS 

    def test_get_current_user_with_token(self):
        """Test profile retrieval using Token Auth header."""
        user = User.objects.create_user(username='apiuser', password='password123')
        token = Token.objects.create(user=user)
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'apiuser')

    def test_unauthenticated_me_request(self):
        """Verify that without a token, access is denied (401)."""
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_remains_consistent(self):
        """Ensure login doesn't generate a NEW token if one already exists."""
        user = User.objects.create_user(username='consistent', password='password123')
        token = Token.objects.create(user=user)
        
        response = self.client.post(self.login_url, {'username': 'consistent', 'password': 'password123'})
        self.assertEqual(response.data['token'], token.key)