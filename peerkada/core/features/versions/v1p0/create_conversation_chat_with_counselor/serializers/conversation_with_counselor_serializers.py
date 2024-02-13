from core.models import PeerkadaAccount, ConversationWithCounselors, CounselorMessages
from rest_framework import serializers
from datetime import datetime
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
    created_at = serializers.DateTimeField(format='%Y-%m-%d-%H:%M:%S')

    class Meta:
        model = CounselorMessages
        fields = [ 'body', 'created_at', 'created_by',]

class ConversationWithCounselorsSerializer(serializers.ModelSerializer):
    users = DisplayPeerkadaAccountSerializer(many=True)
    messages = CounselorMessagesSerializer(many=True, read_only=True, source='messages_counselor')  # Make sure source matches related_name
    created_at = serializers.DateTimeField(format='%Y-%m-%d-%H:%M:%S')
    class Meta:
        model = ConversationWithCounselors
        fields = ['id', 'users', 'created_at', 'modified_at', 'messages']