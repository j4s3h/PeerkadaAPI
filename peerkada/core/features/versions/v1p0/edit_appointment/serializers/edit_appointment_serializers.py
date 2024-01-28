from rest_framework import serializers
from core.models import Appointment, PeerkadaAccount

from rest_framework import serializers
from core.models import Appointment, PeerkadaAccount
import datetime
class CustomDateFormatField(serializers.DateField):
    def to_internal_value(self, value):
        try:
            # Parse the input date in 'YYYY/MM/DD' format
            date_obj = datetime.datetime.strptime(value, '%Y/%m/%d').date()
            return date_obj
        except ValueError:
            raise serializers.ValidationError("Invalid date format. Please use 'YYYY/MM/DD'.")


class DisplayReadPeerkadaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerkadaAccount
        fields = ['id','name', 'username', 'place', 'avatar', 'is_counselor']
class EditAppointmentSerializer(serializers.ModelSerializer):
    date = CustomDateFormatField()
    created_by = DisplayReadPeerkadaAccountSerializer(many=False, read_only = True)
    modified_by = DisplayReadPeerkadaAccountSerializer(many = False, read_only = True)
    class Meta:
        model= Appointment
        fields = ['description','created_by' , 'date', 'modified_by'] 
        


