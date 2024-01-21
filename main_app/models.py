from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.db.models import Avg, Count

# Create your models here.
class Customer(AbstractUser):
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s profile"

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    ingredients = models.TextField(default='')
    price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=0)
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
        return reverse('product_detail', kwargs={'product_id': self.id})
    
    @property
    def total_reviews(self):
        return self.review_set.count()

    @property
    def average_stars(self):
        return self.review_set.aggregate(Avg('stars'))['stars__avg'] or 0

    class Meta:
        ordering = ['name']


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_checkout_id = models.CharField(max_length=100, null=True, blank=True)
    success_date = models.DateTimeField(null=True, blank=True)

    @property
    def total(self):
        items = self.cartitems.all()
        return round(sum([item.price for item in items]), 2)
    
    @property
    def num_of_items(self):
        items = self.cartitems.all()
        if items:
            return sum([item.quantity for item in items])
        else:
            return 0
            
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cart_id': self.id})

    class Meta:
        ordering = ['-success_date']
        


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.PositiveIntegerField(default=0)

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
        return reverse('detail', kwargs={'cartitem_id': self.id})
    
    class Meta:
        ordering = ['-id']

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    stars = models.PositiveIntegerField(default=5)
    content = models.TextField(max_length=250)
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.stars} Stars on {self.date}'
    
    def get_absolute_url(self):
        return reverse('review_delete', kwargs={'fk': self.customer.id,'pk': self.id})
    class Meta:
        ordering = ['-date']

    
