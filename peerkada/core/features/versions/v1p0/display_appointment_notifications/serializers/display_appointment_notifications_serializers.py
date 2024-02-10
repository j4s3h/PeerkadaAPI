from rest_framework import serializers
from core.models import AppointmentNotification

class AppointmentNotificationSerializers(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = AppointmentNotification
        fields = '__all__'