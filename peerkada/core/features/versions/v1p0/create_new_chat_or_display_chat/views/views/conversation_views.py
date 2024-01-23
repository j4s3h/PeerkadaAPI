
from rest_framework.response import Response
from core.models import Conversation, ConversationMessages, PeerkadaAccount
from rest_framework.views import APIView
from peerkada.utilities.constant import *
from django.utils import timezone
from datetime import timedelta
from ..serializers.serializers import ReadConversationSerializer, DisplayConversationSerializer, CreateConversationMessagesSerializer, CreateConversationSerializer
from peerkada.utilities.generate_uid import generate_uuid
from rest_framework.permissions import IsAuthenticated
from django.db import models

class ConversationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        conversations = Conversation.objects.filter(users=user)
        
        # Serialize the conversations data
        serializer = DisplayConversationSerializer(conversations, many=True)
        
        # Create the response data
        data = serializer.data
        message = 'Latest Message'
        status = ok 
        errors = {}
        return Response({'message': message, 'data': data , 'status': status, 'errors': errors})




class ConversationMessageViews(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user

        # Ensure the recipient user ID is provided in the request data
        recipient_id = request.data.get('recipient_id', None)
        
        if not recipient_id:
            data ={}
            message = 'recipient_not_found'
            status  = not_Found
            errors = serializer.errors 
            return Response({'message': message, 'data': data, 'status': status, 'errors': errors})

        # Ensure the recipient user exists
        try:
            recipient_user = PeerkadaAccount.objects.get(id=recipient_id)
        except PeerkadaAccount.DoesNotExist:
            data = {}
            message = 'recipient_not_found'
            status  = not_Found
            errors = serializer.errors 
            return Response({'message': message, 'data': data, 'status': status, 'errors': errors})

        # Get the user who created the message (you may need to adjust this based on your application logic)
        created_by_user_id = request.data.get('created_by_user_id', None)

        # Check if a conversation already exists between the users
        existing_conversation = Conversation.objects.filter(users__in=[user.id, recipient_user.id]).annotate(num_users=models.Count('users')).filter(num_users=2).first()

        if existing_conversation:
            # If a conversation exists, use it
            conversation = existing_conversation
        else:
            serializer = CreateConversationSerializer(data={'users': [user.id, recipient_user.id]})
            if serializer.is_valid():
                # If no conversation exists, create a new one
                conversation = Conversation.objects.create(id=generate_uuid())
                conversation.users.add(user, recipient_user, created_by_user_id)   # Add all users to the conversation
                conversation.save()
            else:
                return Response({'error': 'Invalid data', 'status': 'bad_request', 'errors': serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateConversationMessagesSerializer(data=request.data)
        if serializer.is_valid():
            # Create a new message in the conversation
            message = ConversationMessages.objects.create(
                id=generate_uuid(),
                body=serializer.validated_data['body'],
                created_by=user,
                sent_to=conversation
            )

            # Optionally, you can save the message to update timestamps
            message.save()
            data = serializer.data
            message = 'Succesfully Created'
            status =created
            errors ={}
            return Response({'message': message, 'data': data, 'status': status, 'errors': errors})
        data = {}
        message = 'bad_request'
        status =bad_request
        errors ={}

        return Response({'message': message, 'data': data, 'status': status, 'errors': errors})
        
    
class ReadConversation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id, *args, **kwargs):
        user = request.user

        # Ensure the conversation exists and the user is a part of it
        try:
            conversation = Conversation.objects.get(id=conversation_id, users=user)
        except Conversation.DoesNotExist:
           message = 'DoesnotExist'
           status = not_Found
           data = {}
           errors = {}
           return Response({'message': message, 'data': data, 'status': status, 'errors': errors})

        # Serialize the conversation data
        serializer = ReadConversation(conversation)

        # Create the response data
        response_data = {
            'message': 'Conversation retrieved successfully',
            'data': serializer.data,
            'status': 'ok',
            'errors': {},
        }

        # Return the response
        return Response(response_data)