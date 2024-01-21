import json, time, uuid, stripe
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import SignUpForm, ReviewForm
from .models import Product, Cart, CartItem, Customer, Review


# Create your views here.
def home(request):
    return render(request, 'home.html')

def catalog(request):
    products = Product.objects.all()    
    return render(request, 'products/index.html', {'catalog': products, 'user': request.user})

def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    review_form = ReviewForm
    return render(request, 'products/detail.html', {'product': product, 'user': request.user, 'review_form': review_form})

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_superuser), name='dispatch')
class ProductCreate(CreateView):
    model = Product
    fields = '__all__'
    success_url = '/'

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_superuser), name='dispatch')
class ProductUpdate(UpdateView):
    model = Product
    fields = '__all__'

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_superuser), name='dispatch')
class ProductDelete(DeleteView):
    model = Product
    success_url = '/'

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
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
            
            try:
                session_cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
                user_cart = Cart.objects.filter(customer=request.user, completed=False)
                if user_cart.exists():
                    user_cart.delete()
 
                session_cart.customer = request.user 
                session_cart.save()
            except:
                pass
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

@login_required
def orders_view(request):
    if request.user.is_authenticated:
        orders = Cart.objects.filter(customer=request.user, completed=True)
        print(orders)
    return render(request, 'orders/index.html', {'user': request.user, 'orders': orders})

@login_required
def order_details(request, order_id):
    if request.user.is_authenticated:
        order = Cart.objects.get(stripe_checkout_id= order_id)
    return render(request, 'orders/details.html', {'order': order, 'user': request.user})

# def add_to_cart(request, product_id, action):
def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data['product']
    action = data['action']
    product = Product.objects.get(id=product_id)
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
            if(cartItem.quantity <= 0):
                cartItem.delete()
            print('quantity', cartItem.quantity)
        
        case 'add-to':
            cartItem.increase_quantity()
            products = Product.objects.all()  
            # return render(request, 'products/index.html', {'catalog': products})
                
        case 'del':
            cartItem.delete()
    
    return JsonResponse({'items': cart.num_of_items, 'page': 'cart'}, safe=False)
    # return render(request, 'cart.html')

@login_required
def confirm_payment(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    print(request)
    checkout_session_id = request.GET.get('session_id', None)
    print('checkout id: ',checkout_session_id)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    print(session)
    user = Customer.objects.get(username = session.metadata.user)
    customer = stripe.Customer.retrieve(session.customer)
    cart = Cart.objects.get(customer=user, completed=False)
    cart.stripe_checkout_id = customer.created
    cart.completed = True
    cart.success_date = timezone.now()
    cart.save()
    messages.success(request, 'Payment Successful!')
    return redirect('orders')

@login_required
def create_checkout_session(request, cart_id):
    cart = Cart.objects.get(id=cart_id, completed=False)
    user = request.POST['username']
    price = int(cart.total * 100)
    quantity = cart.num_of_items
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        print('trying')
        checkout_session = stripe.checkout.Session.create(
             line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': f'{quantity} Items',
        },
        'unit_amount': price,
      },
      'quantity': 1,
    }],
            mode='payment',
            customer_creation = 'always',
            success_url= settings.REDIRECT_URL + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url= settings.REDIRECT_URL + '/cart/',
            metadata = {'user': user},
            shipping_address_collection = {
                'allowed_countries': ['US', 'GB', 'CA']
            },
        )
    except Exception as e:
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
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        time.sleep(15)
        cart = Cart.objects.get(stripe_checkout_id=payment_intent.created, completed=False)
        print(cart)
        cart.completed = True
        cart.save()
        print(cart)
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

@login_required
def add_review(request, product_id):
    form = ReviewForm(request.POST)
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.product_id = product_id
        new_review.customer_id = request.user.id
        new_review.date = timezone.now()
        new_review.save()
    return redirect('product_detail', product_id=product_id)

@login_required
def remove_review(request, fk, pk):
    review = Review.objects.get(id=pk)
    if review:
        review.delete()
    else:
        messages.error("The review does not exist!")
    return redirect('product_detail', fk)