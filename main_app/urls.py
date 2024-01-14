from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('products/', views.catalog, name = 'catalog'),
    path('products/<int:product_id>/', views.product_details, name='product_detail'),
    path('signup/', views.signup, name='signup'),
    
]
	
