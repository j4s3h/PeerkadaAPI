from rest_framework import serializers
from core.models import Appointment
import datetime
class CustomDateFormatField(serializers.DateField):
    def to_internal_value(self, value):
        try:
            # Parse the input date in 'YYYY/MM/DD' format
            date_obj = datetime.datetime.strptime(value, '%Y/%m/%d').date()
            return date_obj
        except ValueError:
            raise serializers.ValidationError("Invalid date format. Please use 'YYYY/MM/DD'.")

class CreateAppointmentSerializer(serializers.Serializer):
    date = CustomDateFormatField()
    description = serializers.CharField(max_length=255)

    class Meta:
        model = Appointment
        fields = ['description', 'date', 'counselor']

    def create(self, validated_data):
        # Create and return the Appointment instance
        return Appointment.objects.create(**validated_data)