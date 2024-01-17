import json, time, uuid, stripe
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
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

def confirm_payment(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    print(customer)
    user_id = request.user.user_id 
    print(user_id)
    cart = Cart.objects.get(customer=user_id, completed=False)
    cart.stripe_checkout_id = checkout_session_id
    cart.save()
    messages.success(request, 'Payment Successful!')
    return redirect('orders')

def create_checkout_session(request):
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        print(stripe.api_key)
        print('trying')
        checkout_session = stripe.checkout.Session.create(
             line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': 'T-shirt',
        },
        'unit_amount': 2000,
      },
      'quantity': 1,
    }],
            mode='payment',
            customer_creation = 'always',
            success_url= settings.REDIRECT_URL + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url= settings.REDIRECT_URL + '/cancel/',
        )
        print('maybe')
    except Exception as e:
        print('failed')
        return str(e)

    return redirect(checkout_session.url, code=303)

def checkoutpage(request):
    return render(request, 'checkout.html', {'user': request.user})

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event= None
    try:

        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        cart = Cart.objects.get(stripe_checkout_id=session_id, completed=False)
        cart.completed = True
        cart.save()
    return HttpResponse(status=200)


# class Checkout(View):
#     def post(self, request, *args, **kwargs):
#         checkout_session = stripe.checkout.Session.create(
#             line_items=[
#                 {
#                     # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
#                     'price': '{{PRICE_ID}}',
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success.html',
#             cancel_url=YOUR_DOMAIN + '/cancel.html',
#         )
#         return JsonResponse()