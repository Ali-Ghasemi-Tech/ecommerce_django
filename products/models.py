from django.db import models

# Create your models here.

# The product model represents each of the products that are available for sale in the store.
class Product(models.Model):
    name = models.CharField(max_length=255) #new
    title = models.CharField(max_length=50)
    description = models.TextField(null=True , blank= True)
    unit_price = models.IntegerField()
    inventory = models.PositiveIntegerField(blank=True , default= 0)
    last_update = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='media/product')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True) #new
    category = models.ForeignKey('Category', on_delete=models.CASCADE) #new
    stock = models.PositiveIntegerField() #new
      
    def __str__(self):
        return self.title

#The category model is used to group products.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

# The order model is for storing information related to the user's final purchase.
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,default=1)
    quantity = models.IntegerField(default=1)
    address = models.TextField(max_length=500,default="",blank=True,null=True)
    phone_number = models.CharField(max_length=11,default="",blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    zipcode = models.CharField(max_length=11,default="",blank=True,null=True)

    def __str__(self):
        return self.product.name

# The shopping cart model is for storing the products selected by the user until finalizing the purchase.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"

# This model is used to store each item in the user's shopping cart.
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# This model is for storing information about the products purchased in each order.
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
        
 # This model is for storing payment information related to each order.
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment for Order {self.order.id}"

# The comments and ratings model is for storing user feedback about different products

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"


    
