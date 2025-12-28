import uuid
import requests
from bs4 import BeautifulSoup
from django.db import models
from django.conf import settings

class Link(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='links'
    )
    original_url = models.URLField(max_length=500)
    title = models.CharField(max_length=255, blank=True)
    short_code = models.SlugField(unique=True, blank=True)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = str(uuid.uuid4())[:8]
        
        if not self.title:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(self.original_url, headers=headers, timeout=3)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    if soup.title and soup.title.string:
                        self.title = soup.title.string.strip()
                    else:
                        self.title = self.original_url
                else:
                    self.title = "Untitled Link"
            except Exception:
                self.title = "Error Fetching Title"
                
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or self.original_url