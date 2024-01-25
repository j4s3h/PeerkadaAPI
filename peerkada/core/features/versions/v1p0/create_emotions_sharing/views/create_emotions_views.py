from core.models import PeerkadaAccount, EmotionsSharing
from peerkada.utilities.constant import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from peerkada.utilities.generate_uid import generate_uuid
from ..serializers.create_emotions_serializers import CreateSharingEmotionsSerializer

class CreateEmotionViews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = CreateSharingEmotionsSerializer(data=request.data)

        if serializers.is_valid():
            if 'body' not in request.data:
                message = 'Body is required in form data'
                status= bad_request
                return Response({'message': message, 'status': status})

            uid = generate_uuid()
            emotion = EmotionsSharing.objects.create(
                id=uid,
                body=request.data['body'],
                created_by=request.user
            )

            emotion_data = EmotionsSharing.objects.filter(id=uid).values('body', 'created_by', 'created_at')
            data = emotion_data
            message = 'Successfully Created'
            status = ok
            errors = serializers.errors

            return Response({'message': message, 'data': data, 'status': status, 'errors': errors})

        data = {}
        message = 'Bad request'
        status = bad_request
        errors = serializers.errors

        return Response({'message': message, 'data': data, 'status': status, 'errors': errors})
