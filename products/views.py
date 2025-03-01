from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics

from .models import Product
from .serializers import ProductListSerializer, ProductDeatilSerializer


#The home page view usually displays all the main products or categories.
class ProductListApi(generics.ListAPIView):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductListSerializer


# This view displays the details of a specific product. The user can view information about the product.
class ProductDetailApi(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDeatilSerializer
    lookup_field = 'id'

# This view displays the products based on the specific category selected by the user


def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.product_set.all()  # محصولات این دسته‌بندی را دریافت می‌کنیم
    return render(request, 'shop/category.html', {'category': category, 'products': products})


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
