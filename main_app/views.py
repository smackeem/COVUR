from django.shortcuts import render
from .models import Product, User

catalogs = [
    {'name': 'Day Moisturizer', 'description': 'SPF 15', 'price': 34.99, 'quantity': 40, 'image': 'https://picsum.photos/200/300'},
    {'name': 'Toner', 'description': 'Blemish remover', 'price': 29.99, 'quantity': 40, 'image': 'https://picsum.photos/200/300'},
    {'name': 'Eye Cream', 'description': 'Anti-Age', 'price': 15.99, 'quantity': 40, 'image': 'https://picsum.photos/200/300'},
]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def catalog(request):
    products = Product.objects.all()
    return render(request, 'products/index.html', {'catalog': products})

def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'products/details.html', {'product': product})