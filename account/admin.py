from django.contrib import admin
from .models import Account

# Register your models here.

class CustomeUserAdmin(admin.ModelAdmin):
    list_display = ['username' , 'phone_number' , 'email' , 'is_active']
    list_filter = ['is_active' ]

admin.site.register(Account , CustomeUserAdmin)