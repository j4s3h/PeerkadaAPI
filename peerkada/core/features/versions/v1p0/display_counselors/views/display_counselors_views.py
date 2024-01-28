from core.models import PeerkadaAccount
from peerkada.utilities.constant import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..serializers.display_counselor_serializers import PeerkadaAccountSerializer

class DisplayPeerkadaCounselorViews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        counselors = PeerkadaAccount.objects.filter(is_counselor=True)
        serializer = PeerkadaAccountSerializer(counselors, many=True)
        message = 'Retrieved Succesfully'
        data = serializer.data 
        status = ok 
        errors = {}

        return Response ({"message": message, "data": data, "status": status, "errors": errors })