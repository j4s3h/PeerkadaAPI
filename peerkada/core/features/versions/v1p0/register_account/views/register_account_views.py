from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import PeerkadaAccount
from ..serializer.register_account_serializer import RegisterAccountSerializer
from peerkada.utilities.constant import *
from peerkada.utilities.generate_uid import generate_uuid
from peerkada.utilities.common_errors import validate_birthday, validate_username, validate_email
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError





class RegisterAccountViews(APIView):
    def post(self, request):
        serializer = RegisterAccountSerializer(data=request.data)
        data = {}
        errors = []
        status_code = None
        message = None

        if serializer.is_valid():
            uid = generate_uuid()

            
            try:
                validate_password(request.data['password'])
            except ValidationError as e:
                errors.append({"password": list(e.messages)})

            
            try:
                validate_birthday(serializer.validated_data['birthday'])
            except ValidationError as e:
                errors.append({"birthday": list(e.messages)})

            
            try:
                validate_email(serializer.validated_data['email'])
            except ValidationError as e:
                errors.append({"email": list(e.messages)})

            
            try:
                validate_username(serializer.validated_data['username'])
            except ValidationError as e:
                errors.append({"username": list(e.messages)})

            

            
            if errors:
                status_code = bad_request
                return Response({"message": message, "data": data, "status": status_code, "errors": errors})

            
            encrypted_password = make_password(request.data['password'])

            
            account = PeerkadaAccount.objects.create(
                id=uid,
                name=serializer.validated_data['name'],
                username=serializer.validated_data['username'],
                birthday=serializer.validated_data['birthday'],
                email=serializer.validated_data['email'],
                sex=serializer.validated_data['sex'],
                password=encrypted_password
            )

            
            account_data = PeerkadaAccount.objects.filter(id=uid).values('id', 'username', 'email', 'birthday', 'sex')
            data = account_data.first()  # Use .first() to get the first item from the queryset

            status_code = created
            message = 'Successfully Created'

            return Response({"message": message, "data": data, "status": status_code, "errors": errors})

        errors = serializer.errors
        status_code = bad_request
        return Response({"message": message, "data": data, "status": status_code, "errors": errors})
    
class RegisterAccountCounselorViews(APIView):
    def post(self, request):
        serializer = RegisterAccountSerializer(data=request.data)
        data = {}
        errors = []
        status_code = None
        message = None

        if serializer.is_valid():
            uid = generate_uuid()

            
            try:
                validate_password(request.data['password'])
            except ValidationError as e:
                errors.append({"password": list(e.messages)})

            try:
                validate_birthday(serializer.validated_data['birthday'])
            except ValidationError as e:
                errors.append({"birthday": list(e.messages)})

            try:
                validate_email(serializer.validated_data['email'])
            except ValidationError as e:
                errors.append({"email": list(e.messages)})

            try:
                validate_username(serializer.validated_data['username'])
            except ValidationError as e:
                errors.append({"username": list(e.messages)})

            
            if errors:
                status_code = bad_request
                return Response({"message": message, "data": data, "status": status_code, "errors": errors})

           
            encrypted_password = make_password(request.data['password'])

            
            account = PeerkadaAccount.objects.create(
                id=uid,
                name=serializer.validated_data['name'],
                username=serializer.validated_data['username'],
                birthday=serializer.validated_data['birthday'],
                email=serializer.validated_data['email'],
                sex=serializer.validated_data['sex'],
                password=encrypted_password,
                is_counselor=True
            )

            # Fetch the created account data
            account_data = PeerkadaAccount.objects.filter(id=uid).values('id', 'username', 'email', 'birthday', 'sex')
            data = account_data.first()  # Use .first() to get the first item from the queryset

            status_code = created
            message = 'Successfully Created'

            return Response({"message": message, "data": data, "status": status_code, "errors": errors})

        errors = serializer.errors
        status_code = bad_request
        return Response({"message": message, "data": data, "status": status_code, "errors": errors})
    
    