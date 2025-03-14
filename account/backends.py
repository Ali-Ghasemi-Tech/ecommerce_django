# backends.py
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import Account

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if input is email/phone and sanitize
            user = Account.objects.get(
                Q(username=username) |
                Q(email=username) | 
                Q(phone_number=username)
            )
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            return None
        except Account.MultipleObjectsReturned:
            # Handle edge case (shouldn't happen if email/phone are unique)
            return None