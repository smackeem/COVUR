from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name = 'catalog'),
    path('products/<int:product_id>/', views.product_details, name='product_detail'),
    path('account/signup/', views.signup, name='signup'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('account/login/', views.login_view, name='login'),
    path('account/logout/', views.signout, name = 'logout'),
    path('cart/', views.cart, name='cart'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/<int:order_id>/', views.order_details, name='order_details'),
    path('add/', views.add_to_cart, name='add'),
    path('cart/<int:cart_id>/checkout/', views.create_checkout_session, name='checkout'),
    path('success/', views.confirm_payment, name='success'),
    path('web_hooks/', views.stripe_webhook, name='webhooks'),
    # path('products/<int:products_id>/reviews/create', views.write_review, name='review_create')
]
	
