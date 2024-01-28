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
        serializer = CreateAppointmentSerializer(data=data)

        if serializer.is_valid():
           

            uid = generate_uuid()
            
            formatted_date = serializer.validated_data['date'].strftime('%Y-%m-%d')
            serializer.validated_data['date'] = formatted_date

           
            appointment_instance = serializer.save(
                id=uid,
               
                created_by=PeerkadaAccount.objects.get(id=request.user.id),
            )

            
            response_data = {
                'appointment': {
                    'id': appointment_instance.id,
                    'description': appointment_instance.description,
                    'date': appointment_instance.date,  # Use the formatted date
                    
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
            return Response({"message": message, "data": response_data, "status": created})

        errors = serializer.errors
        status_code = bad_request
        return Response({"status": status_code, "errors": errors})
    