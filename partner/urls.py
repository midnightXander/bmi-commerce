from django.urls import path
from . import views

app_name = 'partner'

urlpatterns = [
    path('register',views.register, name='register'),
    path('login',views.login, name='login'),
    path('logout',views.logout_view, name='logout'),
    path('products/<int:provider_id>',views.get_provider_items, name='products'),
    path('products/add',views.add_product, name='add_product'),
]
