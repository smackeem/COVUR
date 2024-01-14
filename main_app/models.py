from django.contrib.auth.models import AbstractUser
from django.db import models

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
    image = models.ImageField(upload_to='static/product_images/')

    def __str__(self):
        return self.name


# class Cart(models.Model):
#     customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
#     product = models.ForeignKey(Product, on_delete = models.CASCADE)

# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
#     product = models.ForeignKey(Product, on_delete = models.CASCADE)
#     date = models.DateTimeField()
#     total = models.FloatField()
#     status = models.BooleanField(default=False)

# class Review(models.Model):
#     customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
#     product = models.ForeignKey(Product, on_delete = models.CASCADE)
#     stars = models.IntegerField()
#     content = models.TextField(max_length=250)
