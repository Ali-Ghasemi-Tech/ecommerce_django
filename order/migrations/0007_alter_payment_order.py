# Generated by Django 5.1.7 on 2025-03-22 15:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_order_product_orderitem_access_expiry_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='order.order'),
        ),
    ]
