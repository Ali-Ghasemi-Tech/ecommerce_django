from django.shortcuts import render, get_object_or_404,redirect
from rest_framework import serializers
from .models import Product,Review
from .models import Category
from .models import Cart,CartItem
from .models import Order, Payment

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

# This view is for displaying order details and purchase information.
# این ویو برای نمایش جزئیات سفارش و اطلاعات مربوط به خرید است.
def order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order.html', {'order': order})

# The payment view shows the payment process and completion of the purchase.
# ویو پرداخت نمایش فرآیند پرداخت و تکمیل خرید است.

def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        # انجام عملیات پرداخت (در واقع اینجا فقط نمایش داده می‌شود)
        payment = Payment.objects.create(order=order, amount=order.total_price, payment_method='credit_card', status='completed')
        order.status = 'paid'
        order.save()
        return redirect('order', order_id=order.id)
    return render(request, 'shop/payment.html', {'order': order})

# This view allows users to post their opinion and rating for a product.
# این ویو به کاربران اجازه می‌دهد که نظر و امتیاز خود را برای یک محصول ارسال کنند.
def review_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        return redirect('product_detail', product_id=product.id)
    return render(request, 'shop/review.html', {'product': product})

# This view is for searching products based on name or other attributes.
# این ویو برای جستجوی محصولات بر اساس نام یا ویژگی‌های دیگر است.
def search_view(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)  # جستجو بر اساس نام محصول
    else:
        products = Product.objects.all()
    return render(request, 'shop/search.html', {'products': products})




