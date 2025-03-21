from django.db import models
from products.models import Product
from account.models import Account


# Create your models here.

# The order model is for storing information related to the user's final purchase.
class Order(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)  # True for paid, False for unpaid
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total_price(self):
        return sum(item.product.price for item in self.items.all())

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"


# This model is for storing information about the products purchased in each order.
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    access_expiry_date = models.DateTimeField(null=True, blank=True)  # date of the end of the access period

    def __str__(self):
        return f"{self.product.name} in Order {self.order.id}"

