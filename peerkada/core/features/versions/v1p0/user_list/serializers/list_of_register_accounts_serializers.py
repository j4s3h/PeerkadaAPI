from rest_framework import serializers
from  core.models import PeerkadaAccount
class DisplayPeerkadaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerkadaAccount
        fields = ['id', 'name', 'username', 'is_counselor']
        