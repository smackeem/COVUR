from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name = 'catalog'),
    path('products/<int:product_id>/', views.product_details, name='product_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.signout, name = 'logout')
]
	
