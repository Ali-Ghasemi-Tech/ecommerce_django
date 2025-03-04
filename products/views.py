from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import Product, Comment
from .serializers import ProductListSerializer, ProductDetailSerializer, CommentSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework import serializers
from .permissions import IsProductUser
from rest_framework.permissions import AllowAny


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
    serializer_class = ProductDetailSerializer
    lookup_field = 'product_id'

    def get_queryset(self):
        # Use prefetch_related to optimize queries for images, videos, and audios
        return Product.objects.prefetch_related('images', 'videos', 'audios').all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if hasattr(self, 'request'):
            context['request'] = self.request
        return context


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Comment.objects.filter(product_id=product_id)

    def perform_create(self, serializer):

        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")

        serializer.save(user=self.request.user, product=product)

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsProductUser()]
        return [AllowAny()]



