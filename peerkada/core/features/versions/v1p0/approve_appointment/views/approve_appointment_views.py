from rest_framework.response import Response
from rest_framework.views import APIView
from peerkada.utilities.constant import *
from peerkada.utilities.generate_uid import generate_uuid
from core.models import Appointment, AppointmentNotification
from ..serializers.approve_appointment_serializers import AppointmentSerializer

class ApproveAppointmentViews(APIView):
    def get_appointment(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            message = 'This Appointment does not exist'
            data = {}
            status_code = not_Found
            errors = {}
            return Response({"message": message, "data": data, "status": status_code, "errors": errors})

    def post(self, request, appointment_id):
        # Get the appointment using the get_appointment method
        appointment = self.get_appointment(appointment_id)
        
        # Check if the appointment retrieval was successful
        if isinstance(appointment, Response):
            return appointment  # Return the error response if appointment does not exist
        
        try:
            # Perform the approval process
            appointment.is_approved = True
            
            # Set the modified_by field to the user who is making the modification
            appointment.modified_by = request.user
            
            appointment.save()

            # Serialize the appointment before including it in the response
            serializer = AppointmentSerializer(appointment)
            serialized_data = serializer.data
            
            # Create Notification here
            appointment_date = appointment.date  # Assuming date is a field of Appointment
            self.send_notification(appointment, appointment_date)

            message = 'Successful'
            data = serialized_data
            status_code = ok
            errors = {}
            return Response({"message": message, "data": data, "status": status_code, "errors": errors})
        except Exception as e:
            # Handle any other exceptions that might occur during the approval process
            message = 'An error occurred while processing the appointment'
            status_code = bad_request
            data = {}
            errors = {"detail": str(e)}
            return Response({"message": message, "data": data, "status": status_code, "errors": errors})

    def send_notification(self, instance, appointment_date):
        created_by = instance.created_by
        modified_by = self.request.user.username

        # Check if the appointment has been approved
        if instance.is_approved:
            description = f"Your appointment {instance.description} on {appointment_date} has been updated and approved by {modified_by}."
        else:
            description = f"Your appointment {instance.description} on {appointment_date} has been updated by {modified_by}."

        notification = AppointmentNotification.objects.create(
            id=generate_uuid(),  # Assuming generate_uuid() is defined somewhere
            user=created_by,  # Associate the notification with the user who created the appointment
            appointment=instance,
            description=description
        )