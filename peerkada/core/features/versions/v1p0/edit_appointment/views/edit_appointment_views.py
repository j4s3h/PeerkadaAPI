from core.models import Appointment, PeerkadaAccount 
from peerkada.utilities.constant import *
from peerkada.utilities.generate_uid import generate_uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.edit_appointment_serializers import EditAppointmentSerializer

class EditAppointmentViews(APIView):
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

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def put(self, request, pk):
        data = {}
        errors = {}
        status_code = None
        message = None

        appointment = self.get_appointment(pk)

        
        if request.user == appointment.created_by or request.user.is_counselor:
            serializer = EditAppointmentSerializer(appointment, data=request.data)
            if serializer.is_valid():
                
                self.perform_update(serializer)
                data = serializer.data
                message = 'Successfully Updated'
                status_code = ok
            else:
                message = 'Error'
                status_code = bad_request
                errors = serializer.errors
        else:
            message = 'You do not have permission to edit this appointment.'
            status_code = forbidden

        return Response({"message": message, "data": data, "status": status_code, "errors": errors})
