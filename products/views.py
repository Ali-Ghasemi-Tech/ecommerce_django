from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import Product
from .serializers import ProductListSerializer, ProductDeatilSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

#The home page view usually displays all the main products or categories.
class ProductListApi(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = Product.objects.filter(Q(tags__name__icontains=tag) & Q(active=True)).distinct()
        else:
            queryset = Product.objects.filter(active=True)

        return queryset

# This view displays the details of a specific product. The user can view information about the product.
class ProductDetailApi(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDeatilSerializer
    lookup_field = 'id'

# This view displays the products based on the specific category selected by the user


class ProductSearchByTagAPIView(generics.ListAPIView):
    pass

# This view allows users to post their opinion and rating for a product.
# این ویو به کاربران اجازه می‌دهد که نظر و امتیاز خود را برای یک محصول ارسال کنند.
    # def review_view(request, product_id):
    #     product = get_object_or_404(Product, id=product_id)
    #     if request.method == 'POST':
    #         rating = request.POST.get('rating')
    #         comment = request.POST.get('comment')
    #         Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
    #         return redirect('product_detail', product_id=product.id)
    #     return render(request, 'shop/review.html', {'product': product})


