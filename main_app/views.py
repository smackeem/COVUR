import json
import uuid
import stripe
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.conf import settings
from .forms import SignUpForm
from .models import Product, Cart, CartItem


# Create your views here.
def home(request):
    return render(request, 'home.html')

def catalog(request):
    products = Product.objects.all()    
    return render(request, 'products/index.html', {'catalog': products, 'user': request.user})

def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'products/details.html', {'product': product, 'user': request.user})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('/login')
        else:
            messages.warning(request, 'Please check your information and try again!')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())

            cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
            if Cart.objects.filter(customer=request.user, completed=False).exists():
                cart.customer = None
                cart.save()
            else:
                cart.customer = request.user 
                cart.save()

            return redirect('catalog')
        else:
            messages.warning(request, 'Username and Password do not match. Please try again!')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('login')

def cart(request):
    return render(request, 'cart.html', {'user': request.user})

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
                request.session['nonuser'] = str(uuid.uuid4())
                cart = Cart.objects.create(session_id = request.session['nonuser'], completed=False)
        
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