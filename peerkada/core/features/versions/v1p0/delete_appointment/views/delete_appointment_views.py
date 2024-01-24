from core.models import Appointment, PeerkadaAccount 
from peerkada.utilities.constant import *
from peerkada.utilities.generate_uid import generate_uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.delete_appointment_serializers import DeleteAppointmentSerializer

class DeleteAppointmentViews(APIView):
    permission_classes = [IsAuthenticated]

    def get_appointment(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            message = 'This Appointment does not exist'
            data = {}
            status_code = not_Found
            errors = {}
            return Response({"message": message, "data": data, "status": status_code, "errors": errors})

    def delete(self, request, pk):
        data = {}
        errors = {}
        status_code = None
        message = None

        appointment = self.get_appointment(pk)
        # Check if the user making the request is the same as the one who created the appointment
        if request.user != appointment.created_by:
            message = 'You do not have permission to edit this appointment.'
            status =forbidden  # Use appropriate HTTP status code for permission denied
            data ={}
            return Response ({"message": message, "data": data, "status": status, "errors": errors })
        else:
            data = {}
            errors = {}
            status = None
            message = None
            appointment = self.get_appointment(pk)
            appointment.delete()
            message = 'Successfully Deleted'
            status = no_content        
            return Response ({"message": message, "data": data, "status": status, "errors": errors })