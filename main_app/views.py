import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib import messages
from .models import Product, Cart, CartItem
from django.http import JsonResponse
import uuid


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
    cart = None
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(customer=request.user, completed=False)
    return render(request, 'products/index.html', {'cart': cart, 'catalog': products, 'user': request.user})

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
            return redirect('/login')
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'messages': messages})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('catalog')
        else:
            return messages.error()
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('login')

def cart(request):
    cart = None
    cartitems = []
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(customer=request.user, completed=False)
        cartitems = cart.cartitems.all()
    return render(request, 'cart.html', {'user': request.user, 'cart': cart, 'cartitems': cartitems})

def orders_view(request):
    return render(request, 'orders.html', {'user': request.user})

def add_to_cart(request):
    if request.body:
        data = json.loads(request.body)
        product_id = data['product']
        action = data['action']
        product = Product.objects.get(id=product_id)
        print(product, action)
    
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(customer=request.user, completed=False)
        else:
            try:
                cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
            
            except:
                request.session['nonuser'] = str[uuid.uuid4()]
                cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
        cartItem, created = CartItem.objects.get_or_create(cart=cart, product=product)
            
        match action:
            case 'add':
                cartItem.increase_quantity()
                print('quantity', cartItem.quantity)

            case 'sub':
                cartItem.decrease_quantity()
                print('quantity', cartItem.quantity)
                if(cartItem.quantity <= 0):
                    cartItem.delete()
            case 'del':
                cartItem.delete()
        num_of_items = cart.num_of_items     

    return JsonResponse(num_of_items, safe=False)

def confirm_payment(request, cart_id):
    cart = Cart.objects.get(id= cart_id)
    cart.completed = True
    cart.save()
    messages.success(request, 'Payment Successful!')
    return redirect('catalog')