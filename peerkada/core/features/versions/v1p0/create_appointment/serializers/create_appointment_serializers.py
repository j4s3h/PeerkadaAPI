from rest_framework import serializers
from core.models import Appointment

class CreateAppointmentSerializer(serializers.Serializer):
    class Meta:
        model = Appointment
        fields = ['description', 'counselor',]
