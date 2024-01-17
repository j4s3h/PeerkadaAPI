
from rest_framework.response import Response
from core.models import Notification
from rest_framework.views import APIView
from peerkada.utilities.constant import *
from django.utils import timezone
from datetime import timedelta
from ..serializer.read_serializer import NotificationSerializer


class MarkNotificationAsReadView(APIView):
    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()

            # Serialize the notification before including it in the response
            serializer = NotificationSerializer(notification)
            serialized_data = serializer.data

            message = 'Successful'
            data = serialized_data
            status = ok
            errors = {}
            return Response({"message": message, "data": data, "status": status, "errors": errors})
        except Notification.DoesNotExist:
            errors = {}
            message = 'Does Not Exist'
            status = not_Found
            data = {}
            return Response({"message": message, "data": data, "status": status, "errors": errors})