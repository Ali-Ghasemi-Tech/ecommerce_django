from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True , blank= True)
    unit_price = models.IntegerField()
    inventory = models.PositiveIntegerField(blank=True , default= 0)
    last_update = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='media/product')
    
    def __str__(self):
        return self.title

    