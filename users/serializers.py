from rest_framework import serializers
from .models import MemberModel
from django.contrib.auth.password_validation import validate_password
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User


 
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberModel
        exclude = ['is_active' , 'last_login']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
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
        
        if not first_name.isalpha():
            raise serializers.ValidationError('first name should only contain alphabetic characters')
        
        return first_name
    
    def validate_last_name(self , validated_data):
        last_name = validated_data
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
        print(type(validated_data))
        email = None
        if validated_data['email'] == '':
            email = None
        else:
            email = validated_data['email']
        member = MemberModel.objects.create(
            username=validated_data['username'],
            firstname = validated_data['firstname'],
            lastname = validated_data['lastname'],
            password=validated_data['password'] ,
            email = email,
            phone_number = validated_data['phone_number'],
        )
        member.save()
        return member
        
class MemberModelSerailizer(serializers.ModelSerializer):
    class Meta:
        model = MemberModel
        fields = ['id' , 'username']

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberModel
        fields = ['firstname', 'lastname', 'username']

    def validate_username(self, value):
        if not value.isalnum() and '_' not in value:
            raise serializers.ValidationError("Username should only contain alphabetic characters or underscore!")
        if value[0].isdigit():
            raise serializers.ValidationError("Username cannot start with a digit")
        return value

    def validate_first_name(self, value):
        if not value.isalpha(): 
            raise serializers.ValidationError("First name should only contain alphabetic characters")
        return value

    def validate_last_name(self, value):
        if not value.isalpha(): 
            raise serializers.ValidationError("Last name should only contain alphabetic characters")
        return value 


    def update(self, instance, validated_data):
        """
        Update the MemberModel instance.
        """
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance

class LoginSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MemberModel
        fields = ['username' , 'password']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberModel
        fields = '__all__' 
       

class VerifyPhoneSerializer(serializers.Serializer):
    token = serializers.CharField(
        required=True,
        max_length=100,
        error_messages={
            'required': 'Token is required',
            'max_length': 'Token is too long (max 100 characters)'
        }
    )