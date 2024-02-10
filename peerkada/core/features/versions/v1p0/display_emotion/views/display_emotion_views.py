from core.models import EmotionsSharing
from peerkada.utilities.constant import *
from peerkada.utilities.generate_uid import generate_uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.display_emotion_serializers import DisplayEmotionSharingSerializer
from rest_framework.pagination import PageNumberPagination


class DisplayEmotionViews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page

        
        emotions = EmotionsSharing.objects.all().order_by('-created_at')
        result_page = paginator.paginate_queryset(emotions, request)

        serializer = DisplayEmotionSharingSerializer(result_page, many=True)
        data = serializer.data 
        message = 'Success'
        status = ok 
        errors = {}
        return Response({'message': message, 'data': data, 'status': status , 'errors': errors})
      


    