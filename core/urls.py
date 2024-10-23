from django.urls import path
from . import views

app_name = 'moderator'

urlpatterns = [
    path('',views.index, name='index'),
    path('services',views.services, name='services'),
    path('produits',views.products, name='products'),
    path('produits/<str:ref>',views.product, name='product'),
    path('profile',views.profile, name='profile'),
    path('cart',views.cart, name='cart'),
    path('cart/add_item/<int:item_id>',views.add_to_cart, name='add_to_cart'),
    path('cart/remove_item/<int:item_id>',views.remove_from_cart, name='remove_from_cart'),
    path('cart/update_item/<int:item_id>',views.update_cart_item, name='update_cart_item'),
    path('checkout',views.checkout, name='checkout'),
    path('ecommerce/admin/login',views.admin_login, name='ecommerce_login'),
    path('ecommerce/admin/dashboard',views.admin_dashboard, name='ecommerce_dashboard'),
    path('ecommerce/admin/add_product',views.add_product, name='add_product'),

]