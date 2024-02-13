from rest_framework import serializers
from core.models import Appointment, PeerkadaAccount



class DisplayReadPeerkadaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerkadaAccount
        fields = ['id','name', 'username', 'place', 'avatar', 'is_counselor']

class DisplayAppointmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='created_by.name', read_only=True)
    
    class Meta:
        model= Appointment
        fields = ['id', 'date', 'description', 'name', 'is_approved' , 'is_modified']


