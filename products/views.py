from django.shortcuts import render, get_object_or_404
from rest_framework import serializers
from .models import Product

#The home page view usually displays all the main products or categories.
def home(request):
    products = Product.objects.all()  # نمایش تمام محصولات
    return render(request, 'shop/home.html', {'products': products})


# This view displays the details of a specific product. The user can view information about the product.
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})



