from django.contrib import admin
from .models import Account , Profile

# Register your models here.

class CustomeUserAdmin(admin.ModelAdmin):
    list_display = ['username' , 'phone_number' , 'email' , 'is_active' , 'is_staff' , 'is_superuser' , 'date_joined']
    search_fields = ['username' , 'phone_number' , 'email' ]
    list_filter = ['is_active' , 'is_staff' , 'is_superuser']
    filter_horizontal = ['groups' , 'user_permissions']

admin.site.register(Account , CustomeUserAdmin)
admin.site.register(Profile)