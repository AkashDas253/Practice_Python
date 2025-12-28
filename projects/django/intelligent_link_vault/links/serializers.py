from rest_framework import serializers
from .models import Link

class LinkSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')
    full_short_url = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = [
            'id', 'title', 'original_url', 'short_code', 
            'full_short_url', 'clicks', 'owner_name', 'created_at'
        ]
        read_only_fields = ['short_code', 'clicks', 'title']

    def get_full_short_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(f'/go/{obj.short_code}/')
        return f'/go/{obj.short_code}/'