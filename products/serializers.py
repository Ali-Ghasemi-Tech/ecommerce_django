from rest_framework import serializers
from products.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'unit_price', 'category', 'stock', 'image')

    def get_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            return first_image.image.url
        return None


class ProductDeatilSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ('active',)

    def get_images(self, obj):
        images = obj.images.all()
        if images:
            return [image.image.url for image in images]
        return []
