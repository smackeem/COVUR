from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name = 'catalog'),
    path('<int:product_id>/', views.product_details, name='product_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.signout, name = 'logout'),
    path('cart/', views.cart, name='cart'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/<int:order_id>/', views.order_details, name='order_details'),
    path('add/', views.add_to_cart, name='add'),
    path('checkout_view/', views.checkoutpage, name='checkoutpage'),
    path('checkout/', views.create_checkout_session, name='checkout'),
    path('success/', views.confirm_payment, name='success'),
    path('web_hooks/', views.stripe_webhook, name='webhooks')
]
	
