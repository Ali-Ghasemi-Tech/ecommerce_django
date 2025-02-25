from django.shortcuts import render, get_object_or_404,redirect
from rest_framework import serializers
from .models import Product
from .models import Category
from .models import Cart,CartItem

#The home page view usually displays all the main products or categories.
def home(request):
    products = Product.objects.all()  # نمایش تمام محصولات
    return render(request, 'shop/home.html', {'products': products})


# This view displays the details of a specific product. The user can view information about the product.
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

# This view displays the products based on the specific category selected by the user
ef category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.product_set.all()  # محصولات این دسته‌بندی را دریافت می‌کنیم
    return render(request, 'shop/category.html', {'category': category, 'products': products})

# ویو سبد خرید نمایش محصولات انتخابی کاربر در سبد خرید را انجام می‌دهد.
# Shopping cart view displays the products selected by the user in the shopping cart.
def cart_view(request):
    cart = Cart.objects.get(user=request.user)  # سبد خرید کاربر جاری
    return render(request, 'shop/cart.html', {'cart': cart})

# This view allows the user to add a product to her shopping cart.
#این ویو به کاربر اجازه می‌دهد که محصولی را به سبد خرید خود اضافه کند.
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)  # اگر سبد خرید وجود نداشت، ایجاد می‌شود
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)  # اضافه کردن محصول به سبد
    cart_item.quantity += 1  # افزایش تعداد محصول در سبد خرید
    cart_item.save()
    return redirect('cart')

 #This view allows the user to remove a product from her shopping cart.
# این ویو به کاربر اجازه می‌دهد که محصولی را از سبد خرید خود حذف کند.

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()  # حذف محصول از سبد خرید
    return redirect('cart')



