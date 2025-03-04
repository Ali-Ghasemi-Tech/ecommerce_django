from rest_framework import permissions
from .models import Product

class IsProductUser(permissions.BasePermission):

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Get the product ID from the URL
        product_id = view.kwargs.get('product_id')
        if not product_id:
            return False

        # Fetch the product and check if the requesting user is associated with it
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return False

        # Allow only if the user is in the `users` field of the product
        return request.user in product.users.all()