from .models import Cart

def get_cart(request):
    try:
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(customer=request.user, completed=False)
        else:
            cart, created = Cart.objects.get_or_create(session_id = request.session['nonuser'], completed=False)
    except:
        cart = {"num_of_items": 0}
    return {'cart': cart}