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
    
    

    def save(self, *args , **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args , **kwargs)
        

class Profile(models.Model):
    user = models.OneToOneField(MemberModel , on_delete=models.CASCADE)
    email_verification_token = models.CharField(max_length=255 , blank=True , null= True)
    
    def generate_verification_token(self):
        self.email_verification_token = str(uuid.uuid4())
        self.save()
        return self.email_verification_token


