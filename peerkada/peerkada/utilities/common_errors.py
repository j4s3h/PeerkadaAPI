from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import PeerkadaAccount

def validate_birthday(value):
    """
    Validate that the birthday is not in the future.
    """
    today = timezone.localdate()
    if value > today:
        raise ValidationError("Birthday cannot be in the future.")
    return value
def validate_username(value):
    # Check if the username is already taken
    if PeerkadaAccount.objects.filter(username=value).exists():
        raise ValidationError("Username is not available. Please choose a different username.")
    return value

def validate_email(value):
    if PeerkadaAccount.objects.filter(email=value).exists():
        raise ValidationError("Email address is already in use.")
    return value