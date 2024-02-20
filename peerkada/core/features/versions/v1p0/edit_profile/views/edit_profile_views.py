from rest_framework.views import APIView
from rest_framework.response import Response
from peerkada.utilities.constant import *
from core.models import PeerkadaAccount
from ..serializers.edit_profile_serializers import PeerkadaAccountSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, date
class EditProfileViews(APIView):
    permission_classes = [IsAuthenticated]

    def validate_birthday(self, birthday):
        """
        Validate that the birthday is not in the future.
        """
        if isinstance(birthday, str):
            birthday = datetime.strptime(birthday, '%Y/%m/%d').date()
        today = timezone.localdate()
        if birthday > today:
            raise ValidationError("Birthday cannot be in the future.")

    def put(self, request):
        data = {}
        errors = {}
        status_code = None
        message = None
        username = request.user.username
        try:
            peerkada_account = PeerkadaAccount.objects.get(username=username)
        except PeerkadaAccount.DoesNotExist:
            errors['profile'] = 'Profile does not exist'
            return Response({'errors': errors}, status=not_Found)
        # Validate and serialize birthday
        birthday = request.data.get('birthday')
        if birthday:
            try:
                self.validate_birthday(birthday)
            except ValidationError as e:
                errors['birthday'] = e.messages
                return Response({'errors': errors}, status=bad_request)
        serializer = PeerkadaAccountSerializer(instance=peerkada_account, data=request.data, partial=True)
        new_username = request.data.get('username')
        if new_username and new_username != username:  # If username is being updated
            if PeerkadaAccount.objects.filter(username=new_username).exists():
                errors['username'] = 'Username is already taken'
                return Response({'errors': errors}, status=bad_request)

        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            message = 'Profile updated successfully'
            status_code = ok
        else:
            errors = serializer.errors
            status_code = bad_request

        return Response({'data': data, 'errors': errors, 'message': message}, status=status_code)