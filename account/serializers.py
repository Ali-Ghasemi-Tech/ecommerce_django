from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re
from .models import Account

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['is_active' ,'phone_number_active' , 'email_active' , 'last_login' , 'is_staff' , 'is_superuser' , 'date_joined' , 'groups' , 'user_permissions'] 
        extra_kwargs = {
            'password': {'write_only': True},  
        }

    def validate_username(self , validated_data):
        username = validated_data

        if not username.isalnum() and not '_' in username:
            raise serializers.ValidationError('username should only contain alphabetic characters or underscore!')
        if username[0].isdigit():
            raise serializers.ValidationError('username can not start with a digit')
        return username

    
    
    def validate_first_name(self , validated_data):
        first_name = validated_data
        if first_name == '':
            return first_name
        if not first_name.isalpha():
            raise serializers.ValidationError('first name should only contain alphabetic characters')
        
        return first_name
    
    def validate_last_name(self , validated_data):
        last_name = validated_data
        if last_name == '':
            return last_name
        if not last_name.isalpha():
            raise serializers.ValidationError('last name should only contain alphabetic characters')
        
        return last_name 
    def validate_password(self , validated_data):
        password = validated_data

        try:
            validate_password(password)
        except serializers.ValidationError as e:
            self.add_error('password' , e.messages)
        return password 
    
    def validate_phone_number(self , validated_data):
        phone_number = validated_data
        regex = r"^(09)(14|13|12|19|18|17|15|16|11|10|90|91|92|93|94|95|96|32|30|33|35|36|37|38|39|00|01|02|03|04|05|41|20|21|22|23|31|34)\d{7}$"

        if not phone_number.isdigit():
            raise serializers.ValidationError('phone number should only contain digits')
        if len(phone_number) != 11:
            raise serializers.ValidationError('phone number should be 11 digits long')
        if not re.match(regex, phone_number):
            raise serializers.ValidationError('Invalid phone number')
        return phone_number

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        try:
            if password and confirm_password and password != confirm_password:
                raise serializers.ValidationError("Passwords do not match")
            if len(password) < 8:
                raise serializers.ValidationError("Password should be at least 8 characters long")     
            validate_password(password)
            return attrs
        except serializers.ValidationError as e:
            raise e
            
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)



    
    def create(self, validated_data):
    # Remove password from validated_data first
        raw_password = validated_data.pop('password')
        validated_data.pop('confirm_password')  # Remove confirm_password too

        # Create the user WITHOUT setting the password directly
        member = Account.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data.get('email', None),
            phone_number=validated_data['phone_number'],
            # Don't pass password here
        )

        # Hash the password properly
        member.set_password(raw_password)  # <-- This does the hashing
        member.save()

        return member
    
class VerifyPhoneSerializer(serializers.Serializer):
    token = serializers.CharField(
        required=True,
        max_length=100,
        error_messages={
            'required': 'Token is required',
            'max_length': 'Token is too long (max 100 characters)'
        }
    )

class LoginSerializer(serializers.ModelSerializer):
    email_or_phone_or_username = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = Account
        fields = ['email_or_phone_or_username', 'password']

    def validate(self, attrs):
        email_or_phone_or_username = attrs.get('email_or_phone_or_username')
        password = attrs.get('password')

        return attrs

class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'phone_number']
        # Prevent username from being updated
        read_only_fields = ['username']

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)