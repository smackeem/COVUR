from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Customer(AbstractUser):
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s profile"

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, default='')
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images')

    def increase_quantity(self):
        self.quantity += 1
        self.save()

    def decrease_quantity(self):
        self.quantity -= 1
        self.save()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('details', kwargs={'product_id': self.id})



class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_checkout_id = models.CharField(max_length=100, null=True, blank=True)


    @property
    def total(self):
        items = self.cartitems.all()
        return round(sum([item.price for item in items]), 2)
    
    @property
    def num_of_items(self):
        items = self.cartitems.all()
        return sum([item.quantity for item in items])
    
    def get_absolute_url(self):
        return reverse('details', kwargs={'cart_id': self.id})

        


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.IntegerField(default=0)

    def increase_quantity(self):
        self.quantity += 1
        self.product.decrease_quantity()
        self.save()

    def decrease_quantity(self):
        self.quantity -= 1
        self.product.increase_quantity()
        self.save()

    @property
    def price(self):
        return round(self.quantity * self.product.price, 2)

    def __str__(self):
        return f"{self.quantity} {self.product.name}"
    
    def get_absolute_url(self):
        return reverse('details', kwargs={'cartitem_id': self.id})
 
class OrderItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    product_list = models.ForeignKey(OrderItem, on_delete = models.CASCADE)
    date = models.DateTimeField()
    total = models.FloatField()
    status = models.BooleanField(default=False)



# class Review(models.Model):
#     customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
#     product = models.ForeignKey(Product, on_delete = models.CASCADE)
#     stars = models.IntegerField()
#     content = models.TextField(max_length=250)
