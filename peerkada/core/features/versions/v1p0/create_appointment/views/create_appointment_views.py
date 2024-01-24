from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Appointment, PeerkadaAccount
from rest_framework.permissions import IsAuthenticated
from peerkada.utilities.generate_uid import generate_uuid
from peerkada.utilities.constant import *
from ..serializers.create_appointment_serializers import CreateAppointmentSerializer

class CreateAppointmentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = CreateAppointmentSerializer(data=request.data)
        

        if serializer.is_valid():
            # Assuming you have a helper function for generating UUID
            uid = generate_uuid()
            counselor_id = request.data['counselor']
            counselor_instance = PeerkadaAccount.objects.get(id=counselor_id)
            if not counselor_instance.is_counselor:
                data ={}
                message = 'bad request'
                errors = 'User is not Counselor'
                status = bad_request
                return Response({"message": message, "data": data, "status": status, "errors": errors})
            created_by = PeerkadaAccount.objects.get(id=request.user.id)

            appointment = Appointment.objects.create(
                id=uid,
                description=request.data['description'],
                counselor=counselor_instance,
                created_by=created_by,
            )
            created_by_data = {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'birthday': str(request.user.birthday),
                'sex': request.user.sex,
            }
            counselor_data = {
                'id': counselor_instance.id,
                'username': counselor_instance.username,
                'email':counselor_instance.email
            }
            

            
            data = {
            'appointment': {
                'id': uid,
                'description': request.data['description'],
                'counselor': counselor_data,
                'created_by': created_by_data,
            }
        }

            status_code = created
            message = 'Successfully Created'
            return Response({"message": message, "data": data, "status": status_code})

        errors = serializer.errors
        status_code = bad_request
        return Response({"status": status_code, "errors": errors})