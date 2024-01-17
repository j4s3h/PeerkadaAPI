
from rest_framework.response import Response
from core.models import Notification
from rest_framework.views import APIView
from peerkada.utilities.constant import *
from django.utils import timezone
from datetime import timedelta
from ..serializer.get_notification_serializer import NotificationSerializer

class GetNotificationView(APIView):
    def get(self, request):
        user = request.user

        # Get unread notifications
        unread_notifications = Notification.objects.filter(user=user, is_read=False)

        # Get read notifications
        read_notifications = Notification.objects.filter(user=user, is_read=True)

        # Serialize the data
        unread_serializer = NotificationSerializer(unread_notifications, many=True)
        read_serializer = NotificationSerializer(read_notifications, many=True)
        status = "ok"
        message = "User notifications retrieved successfully"
        errors = {}
        data = {
            'unread_count': unread_notifications.count(),
            'unread_notifications': unread_serializer.data,
            'read_count': read_notifications.count(),
            'read_notifications': read_serializer.data,
        }

        return Response({"message": message, "data": data, "status": status, "errors": errors})
