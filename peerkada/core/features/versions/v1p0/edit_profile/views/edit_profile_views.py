from rest_framework.views import APIView
from rest_framework.response import Response
from peerkada.utilities.constant import *
from core.models import PeerkadaAccount
from ..serializers.edit_profile_serializers import PeerkadaAccountSerializer
from rest_framework.permissions import IsAuthenticated
class EditProfileViews(APIView):
    permission_classes = IsAuthenticated
    def put(self, request):
        data = {}
        errors = {}
        status_code = None
        message = None

        # Retrieve the username of the user making the request
        username = request.user.username

        # Retrieve the user's profile based on the username
        try:
            peerkada_account = PeerkadaAccount.objects.get(username=username)
        except PeerkadaAccount.DoesNotExist:
            errors['profile'] = 'Profile does not exist'
            return Response({'errors': errors}, status=404)

        # Create a serializer instance with the instance being edited
        serializer = PeerkadaAccountSerializer(instance=peerkada_account, data=request.data, partial=True)

        # Check if the username field is being updated and if it's already taken
        new_username = request.data.get('username')
        if new_username and new_username != username:  # If username is being updated
            if PeerkadaAccount.objects.filter(username=new_username).exists():
                errors['username'] = 'Username is already taken'
                return Response({'errors': errors}, status=400)

        if serializer.is_valid():
            serializer.save()
            data['profile'] = serializer.data
            message = 'Profile updated successfully'
            status_code = ok
        else:
            errors = serializer.errors
            status_code = bad_request

        return Response({'data': data, 'errors': errors, 'message': message}, status=status_code)