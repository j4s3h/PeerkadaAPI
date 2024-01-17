
from rest_framework.response import Response
from core.models import Notification
from rest_framework.views import APIView
from peerkada.utilities.constant import *
from django.utils import timezone
from datetime import timedelta
from ..serializer.get_notification_serializer import NotificationSerializer

class GetNotificationView(APIView):
    
    def get(self, request):
        user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
        serializer = NotificationSerializer(user_notifications, many=True)
        data = serializer.data
        status = "ok"
        message = "User notifications retrieved successfully"
        errors = {}
        return Response({"message": message, "data": data, "status": status, "errors": errors})