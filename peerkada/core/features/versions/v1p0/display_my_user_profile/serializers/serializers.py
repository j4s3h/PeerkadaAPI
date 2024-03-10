from core.models import PeerkadaAccount, ConversationWithCounselors, CounselorMessages
from rest_framework import serializers
class DisplayPeerkadaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerkadaAccount
        fields = ['id', 'name', 'username', 'place', 'is_counselor', 'birthday', 'bio']