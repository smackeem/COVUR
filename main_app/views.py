from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib import messages
from .models import Product, Cart, CartItem
from django.http import JsonResponse

# catalogs = [
#     {'name': 'Day Moisturizer', 'description': 'SPF 15', 'price': 34.99, 'quantity': 40, 'image': 'https://picsum.photos/200/300'},
#     {'name': 'Toner', 'description': 'Blemish remover', 'price': 29.99, 'quantity': 40, 'image': 'https://picsum.photos/200/300'},
#     {'name': 'Eye Cream', 'description': 'Anti-Age', 'price': 15.99, 'quantity': 40, 'image': 'https://picsum.photos/200/300'},
# ]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def catalog(request):
    products = Product.objects.all()
    print(request.user)
    return render(request, 'products/index.html', {'catalog': products, 'user': request.user})

def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'products/details.html', {'product': product, 'user': request.user})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            print('made,', form)
            return redirect('/products')
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            print(request)
            return redirect('catalog')
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signout(request):
    logout(request)
    print(request)
    return redirect('login')

def cart(request):
    if request.user.is_authenticated:
        cart, created = cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'user': request.user})

def orders_view(request):
    return render(request, 'orders.html', {'user': request.user})

def add_to_cart(request):
    if request.POST:
        product_id = request.POST['product']
        product = Product.objects.get(id=product_id)

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(customer=request.user)
            cartItem, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cartItem.increase_quantity()
            print('quantity', cartItem.quantity)
        return redirect('catalog')