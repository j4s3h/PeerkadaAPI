from rest_framework import serializers
from core.models import Appointment

class CreateAppointmentSerializer(serializers.Serializer):
    date = serializers.DateField(format="%m-%d-%Y")
    class Meta:
        model = Appointment
        fields = ['description','date', 'counselor',]
