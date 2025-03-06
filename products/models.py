from django.db import models
from users.models import MemberModel
from django.core.validators import MinValueValidator, MaxValueValidator
from taggit.managers import TaggableManager

# Create your models here.

# The product model represents each of the products that are available for sale in the store.


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    units_sold = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    tags = TaggableManager()
    text_content = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(MemberModel, related_name='users')

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product/images')

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductVideo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='product/videos')

    def __str__(self):
        return f"Video for {self.product.name}"


class ProductAudio(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='audios')
    audio = models.FileField(upload_to='product/audios')

    def __str__(self):
        return f"Audio for {self.product.name}"




# The comments and ratings model is for storing user feedback about different products

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(MemberModel, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"coment for {self.product.name} by {self.user.username}"
