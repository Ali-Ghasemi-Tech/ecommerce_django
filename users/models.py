from django.db import models
from django.contrib.auth.hashers import make_password
import uuid

# Create your models here.

class MemberModel(models.Model):
    
    username = models.CharField(max_length=200 , unique=True)
    firstname= models.CharField(max_length=200 , blank=True , null = True)
    lastname= models.CharField(max_length=200 , blank=True , null = True)
    is_active = models.BooleanField(default=False)
    email = models.EmailField(blank=True ,null=True , unique=True )
    password= models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True , blank= True)
    phone_number = models.CharField(max_length=11 , unique=True)
    
    

    def save(self, *args , **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args , **kwargs)

    @property
    def is_authenticated(self):
        return True  # Or implement logic based on `is_active`

    @property
    def is_anonymous(self):
        return False
        

class Profile(models.Model):
    user = models.OneToOneField(MemberModel , on_delete=models.CASCADE)
    email_verification_token = models.CharField(max_length=255 , blank=True , null= True)
    phone_verification_token = models.CharField(max_length=255 , blank=True , null= True)
    
    def generate_verification_token(self):
        self.email_verification_token = str(uuid.uuid4())
        self.save()
        return self.email_verification_token

    def generate_phone_verification_token(self):
        verification_token = str(uuid.uuid4())
        self.phone_verification_token = verification_token[0:4]
        self.save()
        return self.phone_verification_token

