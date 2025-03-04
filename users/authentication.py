# authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from django.contrib.auth.models import User
from .models import MemberModel

class DualModelJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            user_type = validated_token.get('user_type')
            
            if user_type == 'admin':
                return User.objects.get(id=user_id)
            elif user_type == 'member':
                return MemberModel.objects.get(id=user_id)
            else:
                raise AuthenticationFailed('Invalid user type')
        except (User.DoesNotExist, MemberModel.DoesNotExist):
            raise AuthenticationFailed('User not found')
        except KeyError:
            raise InvalidToken('Token contains no valid user identification')