from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()

class SystemIntegrationTests(APITestCase):
    
    @patch('requests.get')
    def test_full_user_workflow(self, mock_get):
        """
        Tests the full lifecycle: 
        Register -> Create Link -> Check Profile Link Count
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"<html><title>Integration Success</title></html>"

        reg_url = reverse('user-register-api')
        user_data = {
            'username': 'integrator',
            'email': 'int@test.com',
            'password': 'password123'
        }
        reg_response = self.client.post(reg_url, user_data, format='json')
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)
        token = reg_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        link_url = reverse('link-vault-list')
        link_data = {'original_url': 'https://test-integration.com'}
        
        link_response = self.client.post(link_url, link_data, format='json')
        self.assertEqual(link_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(link_response.data['title'], "Integration Success")

        me_url = reverse('user-me-api')
        me_response = self.client.get(me_url)
        
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.assertEqual(me_response.data['link_count'], 1)
        self.assertEqual(me_response.data['username'], 'integrator')

    def test_cross_user_privacy_integration(self):
        """
        Ensure User A cannot see User B's links via the API.
        """
        user_a = User.objects.create_user(username='user_a', password='password123')
        user_b = User.objects.create_user(username='user_b', password='password123')
        
        from links.models import Link
        Link.objects.create(owner=user_a, original_url="https://usera.com", short_code="linkA")
        
        self.client.force_authenticate(user=user_b)
        
        url = reverse('link-vault-list')
        response = self.client.get(url)
        
        self.assertEqual(len(response.data), 0)