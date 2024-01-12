from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.firstname} {self.lastname}'s profile"

# class Product(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=50)
#     price = models.FloatField()
#     quantity = models.IntegerField()
#     image = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


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
