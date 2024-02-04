from core.models import ConversationWithCounselors, PeerkadaAccount, CounselorMessages
from peerkada.utilities.generate_uid import generate_uuid
from peerkada.utilities.constant import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from ..serializers.conversation_with_counselor_serializers import CreateConversationWithCounselorsSerializer, CreateCounselorMessagesSerializer, ConversationWithCounselorsSerializer

from django.shortcuts import get_object_or_404


class CreateCounselorMessagesViews(APIView):
    def post(self, request, *args, **kwargs):
        data = {}
        user = request.user

        
        potential_recipients = PeerkadaAccount.objects.filter(is_counselor=True)

        
        if not potential_recipients.exists():
            errors = 'No counselors found.'
            status = not_Found
            return Response({"status": status, "errors": errors})

        if user.is_counselor:
            errors = 'You are a counselor; you cannot send a message.'
            status = forbidden
            return Response({"status": status, "errors": errors})

       
        existing_conversation = ConversationWithCounselors.objects.filter(users=user)
        if existing_conversation.exists():
            # Use the existing conversation
            conversation = existing_conversation.first()
        else:
            # Create a new conversation with all counselors
            serializer = CreateConversationWithCounselorsSerializer(
                data={'users': [user.id] + list(potential_recipients.values_list('id', flat=True))}
            )
            if serializer.is_valid():
                conversation = ConversationWithCounselors.objects.create(id=generate_uuid())
                conversation.users.add(user, *potential_recipients)
                conversation.save()
            else:
                message = 'invalid_data'
                status = bad_request
                errors = serializer.errors
                return Response({"message": message, "status": status, "errors": errors})

        # Create a message in the conversation
        serializer = CreateCounselorMessagesSerializer(data=request.data)
        if serializer.is_valid():
            message = CounselorMessages.objects.create(
                id=generate_uuid(),
                body=serializer.validated_data['body'],
                created_by=user,
                sent_to=conversation
            )
            
            message.save()
            received_by_users = message.sent_to.users.exclude(id=user.id)
            received_by_list = [
                {
                    'id': received_by_user.id,
                    'name': received_by_user.name,  # Add the name of the received_by user
                }
                for received_by_user in received_by_users
            ]

            
            response_data = {
                'conversation_id': conversation.id,
                'message_id': message.id,
                'body': serializer.validated_data['body'],
                'sent_by': user.name,  # Assuming 'sent_by' should be the user's ID
                'received_by': received_by_list,
            }
            
            
            message = 'created'
            data = response_data
            status = created
            errors = {}
        else:
            message = 'invalid_data'
            status = bad_request
            errors = serializer.errors

        return Response({"message": message, "data": data, "status": status, "errors": errors})
    
class UserReplyToMessagesViews(APIView):
    def post(self, request, conversation_id, ):
        user = request.user

        try:
            # Try to retrieve the conversation
            conversation = ConversationWithCounselors.objects.get(id=conversation_id, users=user)
        except ConversationWithCounselors.DoesNotExist:
            
            return Response({'detail': 'Conversation not found for the given conversation_id.'}, status=not_Found)

        
        body = request.data.get('body', None)

        if not body:
            return Response({'detail': 'body is a required field.'}, status=bad_request)

        serializer = CreateCounselorMessagesSerializer(data={'body': body})

        if serializer.is_valid():
            message = CounselorMessages.objects.create(
                id=generate_uuid(),
                body=serializer.validated_data['body'],
                created_by=user,
                sent_to=conversation
            )
            
            message.save()
            received_by_users = message.sent_to.users.exclude(id=user.id)
            received_by_list = [
                {
                    'id': received_by_user.id,
                    'name': received_by_user.name,  # Add the name of the received_by user
                }
                for received_by_user in received_by_users
            ]

            
            response_data = {
                'conversation_id': conversation.id,
                'message_id':message.id ,
                'body': serializer.validated_data['body'],
                'sent_by': user.name,  # Assuming 'sent_by' should be the user's ID
                'received_by': received_by_list,
            }
            
            
            message = 'created'
            data = response_data
            status = created
            errors = {}
        else:
            message = 'invalid_data'
            status = bad_request
            errors = serializer.errors

        return Response({"message": message, "data": data, "status": status, "errors": errors})
    
class ReadCounselorMesssagesViews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        conversation_id = request.query_params.get('conversation_id', None)
        is_counselor = user.is_counselor
        status = ok  # Assume success by default
        errors = {}

        if not is_counselor:
            
            try:
                conversation = ConversationWithCounselors.objects.get(users=user)
                serializer = ConversationWithCounselorsSerializer(conversation)
                message = 'Conversation'
                data = serializer.data
            except ConversationWithCounselors.DoesNotExist:
                message = 'not_found'
                data = {}
                status = not_Found  # Set status to not found if conversation is not found

        elif is_counselor and conversation_id:
            # If the user is a counselor and conversation_id is provided, retrieve information about the specified conversation
            try:
                conversation = ConversationWithCounselors.objects.get(id=conversation_id, users=user)
                serializer = ConversationWithCounselorsSerializer(conversation)
                message = 'Conversation'
                data = serializer.data
            except ConversationWithCounselors.DoesNotExist:
                message = 'not_found'
                data = {}
                status = not_Found  # Set status to not found if conversation is not found

        elif is_counselor:
            # If the user is a counselor and no conversation_id is provided, retrieve information about all conversations
            conversations = ConversationWithCounselors.objects.filter(users=user)
            conversations_info = []

            for conversation in conversations:
                latest_message = CounselorMessages.objects.filter(sent_to=conversation).latest('created_at')
                conversation_info = {
                    'conversation_id': conversation.id,                    
                        'content': latest_message.body,
                        'timestamp': latest_message.created_at,
                        'sent_by': latest_message.created_by.name,
                        'is_counselor':latest_message.created_by.is_counselor
                }
                conversations_info.append(conversation_info)

            message = 'Conversations'
            data = conversations_info

        # Return the response
        return Response({"message": message, "is_counselor": is_counselor, "data": data, "status": status, "errors": errors})
        

