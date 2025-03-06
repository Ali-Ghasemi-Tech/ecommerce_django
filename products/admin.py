from django.contrib import admin
from .models import Product , ProductImage , ProductVideo , ProductAudio , Comment 
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVideo)
admin.site.register(ProductAudio)
admin.site.register(Comment)