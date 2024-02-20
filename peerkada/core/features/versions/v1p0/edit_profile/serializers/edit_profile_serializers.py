from rest_framework import serializers
from core.models import PeerkadaAccount

class PeerkadaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerkadaAccount
        fields = [ 'name', 'username', 'birthday']