from django.db import models
from account.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator
from taggit.managers import TaggableManager
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os


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
    users = models.ManyToManyField(Account, related_name='users', blank=True)

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"coment for {self.product.name} by {self.user.username}"



@receiver(post_delete, sender=ProductImage)
def delete_product_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(post_delete, sender=ProductVideo)
def delete_product_video_file(sender, instance, **kwargs):
    if instance.video:
        if os.path.isfile(instance.video.path):
            os.remove(instance.video.path)


@receiver(post_delete, sender=ProductAudio)
def delete_product_audio_file(sender, instance, **kwargs):
    if instance.audio:
        if os.path.isfile(instance.audio.path):
            os.remove(instance.audio.path)
