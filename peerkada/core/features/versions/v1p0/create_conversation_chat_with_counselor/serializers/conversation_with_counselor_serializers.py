from core.models import PeerkadaAccount, ConversationWithCounselors, CounselorMessages
from rest_framework import serializers
class DisplayPeerkadaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerkadaAccount
        fields = ['id', 'name', 'username', 'place', 'avatar', 'is_counselor']

class CreateConversationWithCounselorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationWithCounselors
        fields = ['users', 'created_at', 'modified_at']

  
    

class CreateCounselorMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselorMessages
        fields = [ 'body', 'created_at']



class PeerkadaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerkadaAccount
        fields = [ 'name', 'username', 'is_counselor']

class CounselorMessagesSerializer(serializers.ModelSerializer):
    created_by = PeerkadaAccountSerializer()

    class Meta:
        model = CounselorMessages
        fields = [ 'body', 'created_at', 'created_by',]

class ConversationWithCounselorsSerializer(serializers.ModelSerializer):
    users = DisplayPeerkadaAccountSerializer(many=True)
    messages = CounselorMessagesSerializer(many=True, read_only=True, source='messages_counselor')  # Make sure source matches related_name

    class Meta:
        model = ConversationWithCounselors
        fields = ['id', 'users', 'created_at', 'modified_at', 'messages']