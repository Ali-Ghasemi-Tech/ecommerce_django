from rest_framework import serializers
from products.models import Product , Comment


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'description','unit_price', 'tags', 'units_sold', 'image')

    def get_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            return first_image.image.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    audios = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ('active' , 'users')
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
    

# class CommentSerializer(serializers.ModelSerializer):
#     # Add additional fields for related data (optional)
#     user_username = serializers.CharField(source='user.username', read_only=True)
#     product_name = serializers.CharField(source='product.name', read_only=True)

#     # class Meta:
#     #     model = Comment
#     #     fields = [ 'product', 'product_name', 'user', 'user_username', 
#     #         'rating', 'comment', 'created_at'
#     #     ]
#     #     read_only_fields = ['id', 'created_at', 'user_username', 'product_name'] 

#     # def validate_rating(self, value):
#     #     """
#     #     Ensure the rating is between 1 and 5.
#     #     """
#     #     if value < 1 or value > 5:
#     #         raise serializers.ValidationError("Rating must be between 1 and 5.")
#     #     return value

#     # def create(self, validated_data):
#     #     """
#     #     Create a new comment instance.
#     #     """
#     #     # Ensure the user is set to the requesting user
#     #     user = self.context['request'].user
#     #     validated_data['user'] = user
#     #     return Comment.objects.create(**validated_data)

