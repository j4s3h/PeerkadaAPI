from rest_framework import serializers
from core.models import EmotionsSharing

class CreateSharingEmotionsSerializer(serializers.Serializer):
    class Meta:
        model = EmotionsSharing
        fields = ['body',]
        