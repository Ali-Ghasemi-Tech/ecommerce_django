from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from account.models import Account

# Create your models here.

# The order model is for storing information related to the user's final purchase.
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE,default=1)
    quantity = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    zipcode = models.CharField(max_length=11,default="",blank=True,null=True)

    def __str__(self):
        return self.product.name
    
# This model is for storing information about the products purchased in each order.
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


# This model is used to store each item in the user's shopping cart.
class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


        
 # This model is for storing payment information related to each order.
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment for Order {self.order.id}"

# This model is for storing shipping address details for each order.
class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"Shipping Address for Order {self.order.id}"