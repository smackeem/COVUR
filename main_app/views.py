from django.shortcuts import render

catalogs = [
    {'name': 'Day Moisturizer', 'description': 'SPF 15', 'price': 34.99, 'quantity': 40, 'image': 'https://picsum.photos/200/300'},
    {'name': 'Toner', 'description': 'Blemish remover', 'price': 29.99, 'quantity': 40, 'image': 'https://picsum.photos/200/300'},
    {'name': 'Eye Cream', 'description': 'Anti-Age', 'price': 15.99, 'quantity': 40, 'image': 'https://picsum.photos/200/300'},
]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def catalog(request):
    return render(request, 'products/index.html', {'catalog': catalogs})