from core.models import Appointment, PeerkadaAccount, AppointmentNotification
from peerkada.utilities.constant import *
from peerkada.utilities.generate_uid import generate_uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.edit_appointment_serializers import EditAppointmentSerializer
from datetime import datetime, timedelta
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
        instance = serializer.save(modified_by=self.request.user)
        appointment_date = instance.date.strftime('%Y-%m-%d')  # Format the appointment date
        self.send_notification(instance, appointment_date)

    def send_notification(self, instance, appointment_date):
        created_by = instance.created_by
        modified_by = self.request.user

        # Check if the appointment has been approved
        if instance.is_approved:
            description = f"Your appointment {instance.description} on {appointment_date} has been updated and approved by {modified_by}."
        else:
            description = f"Your appointment {instance.description} on {appointment_date} has been updated by {modified_by}."

        notification = AppointmentNotification.objects.create(
            id=generate_uuid(),
            user=created_by,  # Associate the notification with the user who created the appointment
            appointment=instance,
            description=description
        )

    def put(self, request, pk):
        data = {}
        errors = {}
        status_code = None
        message = None

        appointment = self.get_appointment(pk)

        if request.user == appointment.created_by or request.user.is_counselor:
            serializer = EditAppointmentSerializer(appointment, data=request.data)
            if serializer.is_valid():
                appointment_date = serializer.validated_data['date']
                
                # Check if the user who created the appointment already has an approved appointment within 24 hours of the edited appointment's date
                if appointment.created_by != request.user and appointment_date:
                    existing_appointments = Appointment.objects.filter(
                        created_by=appointment.created_by,
                        is_approved=True,
                        date__gte=appointment_date - timedelta(days=1),
                        date__lte=appointment_date + timedelta(days=1)
                    )
                    if existing_appointments.exists():
                        return Response({"message": "The creator of this appointment already has an approved appointment within 24 hours of the edited date.", "status": "bad_request"}, status=400)

                self.perform_update(serializer)
                data = serializer.data
                message = 'Successfully Updated'
                status_code = ok
                errors =serializer.errors
                return Response({"message": message, "data": data, "status": status_code, "errors": errors})
            else:
                data={}
                message = 'Error'
                status_code = bad_request
                errors = serializer.errors
                return Response({"message": message, "data": data, "status": status_code, "errors": errors})
        else:
            message = 'You do not have permission to edit this appointment.'
            status_code = forbidden

        return Response({"message": message, "data": data, "status": status_code, "errors": errors})
