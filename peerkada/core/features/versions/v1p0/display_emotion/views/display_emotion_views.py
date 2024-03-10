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
      


class DisplayEmotionIndivViews(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_emotion_sharing(self, pk):
        try:
            emotion_sharing = EmotionsSharing.objects.filter(pk=pk)
            return emotion_sharing
        except EmotionsSharing.DoesNotExist:
            data = {}
            message = 'Oops'
            errors = {}
            status = not_Found
            return Response({"message": message, "data": data, "status": status, "errors": errors})
    def get(self, request,pk):
        emotion_sharing = self.get_emotion_sharing(request.user)
        if emotion_sharing is not None:
            emotion = EmotionsSharing.objects.get(id=pk)
            serializer = DisplayEmotionSharingSerializer(emotion)
            status = ok
            message = 'Successfully Retrieved'
            data = serializer.data
            errors = {}
            return Response({"message": message, "data": data, "status": status, "errors": errors})
        else:
            message = 'Oops'
            data = {}
            errors = {}
            status = not_Found  
            return Response({"message": message, "data": data, "status": status, "errors": errors})
class DisplayEmotionByUserViews(APIView):
   
    permission_classes = [IsAuthenticated]
    
    def get_emotion_sharing(self, user_id):
        try:
            emotion_sharing = EmotionsSharing.objects.filter(created_by=user_id).order_by('-created_at')
            return emotion_sharing
        except EmotionsSharing.DoesNotExist:
            return None
            
    def get(self, request,user_id):
        emotion_sharing = self.get_emotion_sharing(user_id)
        if emotion_sharing is not None:
            serializer = DisplayEmotionSharingSerializer(emotion_sharing, many=True)
            status = ok
            message = 'Successfully Retrieved'
            data = serializer.data
            errors = {}
            return Response({"message": message, "data": data, "status": status, "errors": errors})
        else:
            message = 'Oops'
            data = {}
            errors = {}
            status = not_Found  
            return Response({"message": message, "data": data, "status": status, "errors": errors})


