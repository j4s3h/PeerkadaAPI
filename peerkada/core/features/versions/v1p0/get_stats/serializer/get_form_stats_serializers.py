from rest_framework import serializers
from core.models import PeerkadaAccount, Stats

class DisplayFormStatsSerializer(serializers.ModelSerializer):
    total_score = serializers.IntegerField()
    class Meta:
        model = Stats
        fields = '__all__'


   