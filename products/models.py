from django.db import models
from users.models import MemberModel
from django.contrib.auth.models import User

# Create your models here.

# The product model represents each of the products that are available for sale in the store.
class Product(models.Model):
    name = models.CharField(max_length=255) #new
    title = models.CharField(max_length=50)
    description = models.TextField(null=True , blank= True)
    unit_price = models.IntegerField()
    inventory = models.PositiveIntegerField(blank=True , default= 0)
    last_update = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='media/product')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True) #new
    category = models.ForeignKey('Category', on_delete=models.CASCADE) #new
    stock = models.PositiveIntegerField() #new
      
    def __str__(self):
        return self.title

#The category model is used to group products.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

# The comments and ratings model is for storing user feedback about different products

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"


    
