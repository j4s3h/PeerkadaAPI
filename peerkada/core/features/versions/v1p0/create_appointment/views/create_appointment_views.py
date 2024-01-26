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
            if 'counselor' not in data:
                message = 'counselor is required in form data'
                status = bad_request
                errors = {}
                return Response({'message': message, 'status': status, 'errors': errors})

            uid = generate_uuid()
            counselor_id = data['counselor']

            try:
                counselor_instance = PeerkadaAccount.objects.get(id=counselor_id)

                if not counselor_instance.is_counselor:
                    message = 'bad request'
                    errors = 'User is not Counselor'
                    status = bad_request
                    return Response({"message": message, "data": {}, "status": status, "errors": errors})
            except PeerkadaAccount.DoesNotExist:
                # Handle the case where PeerkadaAccount with the specified counselor_id does not exist
                message = 'bad request'
                errors = 'PeerkadaAccount matching query does not exist.'
                status = bad_request
                return Response({"message": message, "data": {}, "status": status, "errors": errors})

            # Ensure date is in 'YYYY-MM-DD' format before saving
            formatted_date = serializer.validated_data['date'].strftime('%Y-%m-%d')
            serializer.validated_data['date'] = formatted_date

           
            appointment_instance = serializer.save(
                id=uid,
                counselor=counselor_instance,
                created_by=PeerkadaAccount.objects.get(id=request.user.id),
            )

            
            response_data = {
                'appointment': {
                    'id': appointment_instance.id,
                    'description': appointment_instance.description,
                    'date': appointment_instance.date,  # Use the formatted date
                    'counselor': {
                        'id': counselor_instance.id,
                        'username': counselor_instance.username,
                        'email': counselor_instance.email,
                    },
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
    