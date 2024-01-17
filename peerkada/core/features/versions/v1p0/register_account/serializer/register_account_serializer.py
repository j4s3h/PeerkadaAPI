from rest_framework import serializers
from core.models import PeerkadaAccount
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegisterAccountSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(format="%m-%d-%Y")
    
    # New fields for password and password confirmation
    password = serializers.CharField(write_only=True, required=True, max_length=50)
    password_confirm = serializers.CharField(write_only=True, required=True, max_length=50)

    class Meta:
        model = PeerkadaAccount
        fields = ['name', 'username', 'place', 'birthday', 'email', 'sex', 'created', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Remove the password_confirm field as it's not part of the model
        validated_data.pop('password_confirm', None)

        # Validate and encrypt the password
        try:
            validate_password(validated_data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        validated_data['password'] = make_password(validated_data['password'])

        return super().create(validated_data)