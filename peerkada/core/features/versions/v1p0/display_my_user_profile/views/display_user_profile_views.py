from rest_framework.response import Response
from rest_framework.views import APIView
from peerkada.utilities.constant import *
from ..serializers.serializers import DisplayPeerkadaAccountSerializer

class DisplayMyProfileViews(APIView):
    def get(self, request):
        user = request.user
        serializer =DisplayPeerkadaAccountSerializer(user)
        message = 'Successful'
        
        data = serializer.data
        status = ok
        errors = {}
        return Response({"message": message, "data": data, "status": status, "errors": errors})