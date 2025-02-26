from django.shortcuts import render , redirect , get_object_or_404
from .models import Cart , Product , CartItem ,Order


# Create your views here.

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