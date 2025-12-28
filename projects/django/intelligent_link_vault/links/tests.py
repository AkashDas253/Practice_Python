from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch
from .models import Link

User = get_user_model()

class LinkComprehensiveTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password123")
        self.other_user = User.objects.create_user(username="hacker", password="password123")
        
        self.client.login(username="tester", password="password123")
        
        self.link = Link.objects.create(
            owner=self.user,
            original_url="https://www.python.org",
            short_code="py-link"
        )

    # MODEL & SCRAPER TESTS 

    @patch('requests.get')
    def test_link_creation_scrapes_title(self, mock_get):
        """Test that the save() method scrapes titles correctly using a mock."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"<html><title>Python Success</title></html>"

        new_link = Link.objects.create(
            owner=self.user,
            original_url="https://fake-link.com"
        )
        self.assertEqual(new_link.title, "Python Success")
        self.assertEqual(len(new_link.short_code), 8)

    # WEB REDIRECT TESTS 

    def test_redirect_view_increments_clicks(self):
        """Test the public redirect increments the click counter."""
        url = reverse('link-redirect', kwargs={'short_code': self.link.short_code})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.link.original_url)
        
        self.link.refresh_from_db()
        self.assertEqual(self.link.clicks, 1)

    # API ENDPOINT TESTS 

    def test_api_list_only_shows_owned_links(self):
        """Security check: Users should not see other users' links in the API."""
        Link.objects.create(owner=self.other_user, original_url="https://secret.com")
        
        url = reverse('link-vault-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['short_code'], "py-link")

    def test_api_create_link(self):
        """Test creating a link via JSON POST."""
        url = reverse('link-vault-list')
        data = {"original_url": "https://www.github.com"}
        
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = b"<html><title>GitHub</title></html>"
            response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "GitHub")
        self.assertEqual(Link.objects.filter(owner=self.user).count(), 2)

    def test_api_delete_link(self):
        """Test deleting a link via the API using short_code lookup."""
        url = reverse('link-vault-detail', kwargs={'short_code': self.link.short_code})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Link.objects.count(), 0)

    def test_unauthorized_api_access(self):
        """Ensure logged-out users can't touch the API."""
        self.client.logout()
        url = reverse('link-vault-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)