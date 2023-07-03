from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='static/img/')
    def __str__(self):
        return self.name


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_price=models.FloatField()
    orderd_at=models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f' order {self.id}'


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f'{self.product.name } - {self.quantity}'
  

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f' {self.id} - {self.quantity}'


def get_catitems(cart):
    cart_items = CartItem.objects.filter(cart=cart)
    