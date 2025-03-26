from django.db import models
from order.models import Order
from account.models import Account

# Create your models here.


class PaymentTransaction(models.Model):
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order , on_delete=models.DO_NOTHING)
    amount = models.IntegerField()  # Amount in rial
    authority = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)