from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Appointment, PeerkadaAccount
from rest_framework.permissions import IsAuthenticated
from peerkada.utilities.generate_uid import generate_uuid
from peerkada.utilities.constant import *
from ..serializers.create_appointment_serializers import CreateAppointmentSerializer
from datetime import datetime, timedelta


class CreateAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = CreateAppointmentSerializer(data=data)

        if serializer.is_valid():
            appointment_date = serializer.validated_data['date']
            
            if appointment_date < datetime.now().date():
                return Response({"message": "Cannot create appointments in the past.", "status": bad_request})

            existing_appointments = Appointment.objects.filter(
                created_by=request.user,
                is_approved=True,
                date__gte=appointment_date - timedelta(days=1),
                date__lte=appointment_date + timedelta(days=1)
            )

            if existing_appointments.exists():
                return Response({"message": "You already have an approved appointment within 24 hours of this date.", "status":bad_request})

            uid = generate_uuid()
            appointment_instance = serializer.save(
                id=uid,
                created_by=request.user,
            )

            response_data = {
                'appointment': {
                    'id': appointment_instance.id,
                    'description': appointment_instance.description,
                    'date': appointment_instance.date.strftime('%Y-%m-%d'),  
                    'created_by': {
                        'id': request.user.id,
                        'username': request.user.username,
                        'email': request.user.email,
                        'birthday': str(request.user.birthday),
                        'sex': request.user.sex,
                    },
                }
            }

            message = 'Successfully Created'
            status = 201
            return Response({"message": message, "data": response_data, "status": status})

        errors = serializer.errors
        return Response({"status": 400, "errors": errors})