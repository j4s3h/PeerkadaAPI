from rest_framework import serializers
from core.models import  PeerkadaAccount, EmotionsSharing
class DisplayReadPeerkadaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerkadaAccount
        fields = ['id','name', 'username', 'place', 'avatar', 'is_counselor']

class DisplayEmotionSharingSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='created_by.name', read_only=True)
    class Meta:
        model = EmotionsSharing
        fields = ['id','body', 'comments', 'like', 'created_at', 'created_by', 'name']



