from rest_framework import serializers
from core.models import Conversation, ConversationMessages, PeerkadaAccount

class PeerkadaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerkadaAccount
        fields = ['id', 'name', 'username', 'place', 'avatar', 'is_counselor']



class CreateConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['users', 'created_at', 'modified_at']

  
    

class CreateConversationMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationMessages
        fields = [ 'body', 'created_at']

class ConversationMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        created_by = PeerkadaAccountSerializer()
        sent_to = PeerkadaAccountSerializer()
        model = ConversationMessages
        fields = ['id', 'body', 'created_at', 'created_by','sent_to']

    
class DisplayConversationSerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'users', 'created_at', 'modified_at', 'latest_message']

    def get_latest_message(self, instance):
        latest_message = instance.messages.last()
        if latest_message:
            return ConversationMessagesSerializer(latest_message).data
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['latest_message'] = self.get_latest_message(instance)
        return data

class ReadConversationSerializer(serializers.ModelSerializer):
    messages = ConversationMessagesSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'users', 'created_at', 'modified_at','messages' ]