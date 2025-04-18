from rest_framework import serializers
from products.models import Product, Comment
from django.db.models import Avg


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'short_description', 'price', 'tags', 'units_sold', 'image')

    def get_tags(self, obj):
        return list(obj.tags.names())

    def get_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            return first_image.image.url
        return None

    def get_short_description(self, obj):
        words = obj.description.split()[:6]
        return ' '.join(words)


class ProductDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    audios = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    text_content = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'images', 'videos', 'audios', 'text_content', 'comment_count', 'average_rating',
                  'units_sold']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.user = self.context.get('request').user if self.context.get('request') else None

    def _is_user_associated(self, obj):
        if self.user and self.user.is_authenticated:
            return obj.users.filter(id=self.user.id).exists()
        return False

    def get_images(self, obj):
        if self._is_user_associated(obj):
            images = obj.images.all()
            return [image.image.url for image in images]
        return []

    def get_videos(self, obj):
        if self._is_user_associated(obj):
            videos = obj.videos.all()
            return [video.video.url for video in videos]
        return []

    def get_audios(self, obj):
        if self._is_user_associated(obj):
            audios = obj.audios.all()
            return [audio.audio.url for audio in audios]
        return []
    
    def get_text_content(self,obj):
        if self._is_user_associated(obj):
            return obj.text_content

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_average_rating(self, obj):
        return obj.comments.aggregate(Avg('rating'))['rating__avg']


class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Comment
        fields = ['product_name', 'user_username', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at', 'user_username', 'product_name']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
