from rest_framework.views import APIView
from core.models import Appointment, PeerkadaAccount
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from peerkada.utilities.constant import *
from ..serializers.display_appointment_serializers import DisplayAppointmentSerializer
class DisplayAppointmentViews(APIView):
    def get_appointments(self, user):
        if user.is_counselor:
            # If the user is a counselor, retrieve all appointments
            appointments = Appointment.objects.all().order_by('created_at')
        else:
            # If the user is not a counselor, retrieve appointments created by them
            appointments = Appointment.objects.filter(created_by=user).order_by('created_at')
        return appointments

    def get(self, request):
        requesting_user = request.user
        appointments = self.get_appointments(requesting_user)

        # Serialize the list of instances, not the queryset itself
        serializer = DisplayAppointmentSerializer(appointments, many=True)
        data = serializer.data

        return Response({
            "message": "Appointment requests retrieved successfully",
            "data": data,
            "status": ok,
            "errors": {}
        })