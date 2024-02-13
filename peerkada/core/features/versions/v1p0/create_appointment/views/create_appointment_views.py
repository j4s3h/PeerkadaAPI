from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Appointment, PeerkadaAccount
from rest_framework.permissions import IsAuthenticated
from peerkada.utilities.generate_uid import generate_uuid
from peerkada.utilities.constant import *
from ..serializers.create_appointment_serializers import CreateAppointmentSerializer
from datetime import datetime


class CreateAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get user's existing appointments
        existing_appointments = Appointment.objects.filter(created_by=request.user)

        # Check if there are any future appointments
        has_future_appointment = existing_appointments.filter(date__gte=datetime.now()).exists()

        # Check if there are any pending (waiting for approval) appointments
        has_pending_appointment = existing_appointments.filter(is_approved=False).exists()

        # If there is a pending appointment in the future, prevent user from creating a new one
        if has_pending_appointment and has_future_appointment:
            return Response({"message": "You already have a future appointment waiting for admin's approval. Please wait for admin's approval.", "status": bad_request})

        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = CreateAppointmentSerializer(data=data)

        if serializer.is_valid():
            appointment_date = serializer.validated_data['date']

            if appointment_date < datetime.now().date():
                return Response({"message": "Cannot create appointments in the past.", "status": bad_request})

            uid = generate_uuid()
            formatted_date = appointment_date.strftime('%Y-%m-%d')
            serializer.validated_data['date'] = formatted_date
            serializer.validated_data['is_modified'] = False
            appointment_instance = serializer.save(
                id=uid,
                created_by=PeerkadaAccount.objects.get(id=request.user.id),
            )

            response_data = {
                'id': appointment_instance.id,
                'description': appointment_instance.description,
                'date': appointment_instance.date,  # Use the formatted date

                'created_by': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'birthday': str(request.user.birthday),
                    'sex': request.user.sex,
                }
            }

            message = 'Successfully Created'
            return Response({"message": message, "data": response_data, "status": created})

        errors = serializer.errors
        status = bad_request
        return Response({"status": status, "errors": errors})