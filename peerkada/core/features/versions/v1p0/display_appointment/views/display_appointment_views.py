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
            serializer = DisplayAppointmentSerializer(appointments, many=True)
        else:
            # If the user is not a counselor, retrieve the most recent appointment created by them
            appointment = Appointment.objects.filter(created_by=user).order_by('-created_at').first()
            if appointment is not None:
                serializer = DisplayAppointmentSerializer(appointment)
            else:
                serializer = None
        return serializer

    def get(self, request):
        requesting_user = request.user
        serializer = self.get_appointments(requesting_user)
        
        if serializer is not None:
            data = serializer.data
        else:
            data = []

        return Response({
            "message": "Appointment requests retrieved successfully",
            "data": data,
            "status": ok,  
            "errors": {}  })