from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import PeerkadaAccount
from ..serializers.list_of_register_accounts_serializers import DisplayPeerkadaAccountSerializer
from peerkada.utilities.constant import *
from rest_framework.permissions import IsAuthenticated






class ListOfRegisteredAccounts(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Check if the user is a counselor
        if user.is_counselor:
            registered_accounts = PeerkadaAccount.objects.all()
            registered_accounts = [account for account in registered_accounts if account.id or account.name]
            serializer = DisplayPeerkadaAccountSerializer(registered_accounts, many=True)
            status = 'ok'  # Adjusted status variable
            data = serializer.data  
            return Response({'message': 'Success', 'data': data, 'status': status})
        else:
            data = {}
            status = forbidden
            return Response({'message': 'Forbidden', 'data': data, 'status': status})
