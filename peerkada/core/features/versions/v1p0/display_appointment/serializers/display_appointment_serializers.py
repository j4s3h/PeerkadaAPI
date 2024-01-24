from rest_framework import serializers
from core.models import Appointment, PeerkadaAccount


class DisplayReadPeerkadaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerkadaAccount
        fields = ['id','name', 'username', 'place', 'avatar', 'is_counselor']
class DisplayAppointmentSerializer(serializers.ModelSerializer):
    created_by = DisplayReadPeerkadaAccountSerializer(many=False, read_only = True)
    counselor = DisplayReadPeerkadaAccountSerializer(many=False, read_only = True)
    class Meta:
        model= Appointment
        fields = ['id','description','created_by' , 'counselor'] 
        


