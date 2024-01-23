from core.models import Stats
from rest_framework import serializers

class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = '__all__'



class AveragesSerializer(serializers.Serializer):
    worried_average_weekly = serializers.FloatField()
    happy_average_weekly = serializers.FloatField()
    angry_average_weekly = serializers.FloatField()
    sad_average_weekly = serializers.FloatField()
    positive_average_weekly = serializers.FloatField()
    overall_average_weekly = serializers.FloatField()

    worried_average_monthly = serializers.FloatField()
    happy_average_monthly = serializers.FloatField()
    angry_average_monthly = serializers.FloatField()
    sad_average_monthly = serializers.FloatField()
    positive_average_monthly = serializers.FloatField()
    overall_average_monthly = serializers.FloatField()

class OverallAveragesSerializer(serializers.Serializer):
    overall_average = serializers.FloatField()