from django.contrib import admin
from .models import Link 

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_code', 'clicks', 'owner', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('original_url', 'title')
    readonly_fields = ('clicks', 'short_code')