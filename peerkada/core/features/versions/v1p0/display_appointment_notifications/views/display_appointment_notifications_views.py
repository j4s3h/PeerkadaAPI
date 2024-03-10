from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.display_appointment_notifications_serializers import AppointmentNotificationSerializers
from core.models import AppointmentNotification
from peerkada.utilities.constant import *
class DisplayAppointmentNotificationView(APIView):
    def get(self, request):
            
        user = request.user

        # Get unread notifications
        unread_notifications = AppointmentNotification.objects.filter(user=user, is_read=False).order_by('-created_at')

        # Get read notifications
        read_notifications = AppointmentNotification.objects.filter(user=user, is_read=True).order_by('-created_at')

        # Serialize the data
        unread_serializer = AppointmentNotificationSerializers(unread_notifications, many=True)
        read_serializer = AppointmentNotificationSerializers(read_notifications, many=True)
        status = ok
        message = "User notifications retrieved successfully"
        errors = {}
        data = {
            'unread_count': unread_notifications.count(),
            'unread_notifications': unread_serializer.data,
            'read_count': read_notifications.count(),
            'read_notifications': read_serializer.data,
        }
        return Response({"message": message, "data": data, "status": status, "errors": errors})





class MarkAppointmentNotificationReadView(APIView):
    def post(self, request, notification_id):
        try:
            notification = AppointmentNotification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()

            # Serialize the notification before including it in the response
            serializer = AppointmentNotificationSerializers(notification)
            serialized_data = serializer.data

            message = 'Successful'
            data = serialized_data
            status = ok
            errors = {}
            return Response({"message": message, "data": data, "status": status, "errors": errors})
        except AppointmentNotification.DoesNotExist:
            errors = {}
            message = 'Does Not Exist'
            status = not_Found
            data = {}
            return Response({"message": message, "data": data, "status": status, "errors": errors})