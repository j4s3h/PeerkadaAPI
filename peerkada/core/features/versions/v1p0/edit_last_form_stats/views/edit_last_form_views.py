from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Stats, PeerkadaAccount, Notification
from django.db import models
from peerkada.utilities.common_errors import *
from peerkada.utilities.constant import *
from peerkada.utilities.generate_uid import generate_uuid
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from ..serializers.edit_last_form_serializer import EditFormStatsSerializer
from django.forms.models import fields_for_model


class EditFormStatsViews(APIView):
    permission_classes = [IsAuthenticated]

    def calculate_total_score(self, stat):
        total_score = 0
        for field in stat._meta.get_fields():
            if (
                field.name not in ['created_by', 'id']
                and not field.is_relation
                and isinstance(field, models.IntegerField)
            ):
                total_score += int(getattr(stat, field.name, 0))

        setattr(stat, 'total_score', total_score)

    def check_mental_wellbeing(self, stat):
        # Calculate or retrieve total score
        self.calculate_total_score(stat)

        # Define your mental well-being criteria
        if 60 <= stat.total_score <= 70:
            message = "You are in the optimum state of mental wellbeing! Keep it up!"
        elif 45 <= stat.total_score <= 55:
            message = "You are in a good state of mental wellbeing!"
        elif 14 <= stat.total_score <= 42:
            message = "You are showing signs of being mentally unwell. Please take a quick rest and meditate."
            return

        # Retrieve user's notifications
        user_notifications = Notification.objects.filter(user=stat.created_by).order_by('created_at')

        uid =generate_uuid()
        # Create a notification for the user
        new_notification = Notification.objects.create(user=stat.created_by,id= uid, message=message)

        # Delete the oldest notification if there are more than 10
        if user_notifications.count() > 10:
            oldest_notification = user_notifications.first()
            oldest_notification.delete()


    def put(self, request):
            data = request.data.copy()
            data['created_by'] = request.user.id


            

            # Check if the user already has existing Stats data
            existing_stats = Stats.objects.filter(created_by=request.user).first()

            if existing_stats:
                # User has existing Stats data, proceed with the update
                serializer = EditFormStatsSerializer(existing_stats, data=data)

                if serializer.is_valid():
                    # Update existing Stats instance with new data
                    serializer.save()

                    # Perform mental well-being check and create notification
                    self.check_mental_wellbeing(existing_stats)

                    created_by_data = {
                        'id': request.user.id,
                        'username': request.user.username,
                        'email': request.user.email,
                        'birthday': str(request.user.birthday),
                        'sex': request.user.sex,
                    }

                    response_data = {
                        'id': existing_stats.id,
                        'created_by': created_by_data,
                        'optimism': existing_stats.optimism,
                        'usefulness': existing_stats.usefulness,
                        # ... (include other fields)
                        'total_score': existing_stats.total_score,
                    }

                    message = 'Successfully updated'
                    status = ok  # Using HTTP_200_OK constant
                    errors = {}

                    return Response({'message': message, 'data': response_data, 'status': status, 'errors': errors})

                message = 'Oops'
                errors = serializer.errors
                status = forbidden  
                return Response({'message': message, 'data': data, 'status': status, 'errors': errors})

            else:
                
                message = 'Please answer the form first'
                status = bad_request 
                errors = {'detail': message}

                return Response({'message': message, 'status': status, 'errors': errors})