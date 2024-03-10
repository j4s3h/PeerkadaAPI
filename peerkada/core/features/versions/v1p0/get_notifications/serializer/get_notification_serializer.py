from rest_framework import serializers
from core.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Notification
        fields = '__all__'