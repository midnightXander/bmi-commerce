from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.index, name='index'),
    path('upload', views.upload,name = 'upload'),
    path('services',views.services, name='services'),
    path('notre-equipe',views.team, name='team'),
    path('produits',views.products, name='products'),
    path('produits/<str:ref>',views.product, name='product'),
    path('profile',views.profile, name='profile'),
    path('contact',views.contact, name='contact'),
    path('cart',views.cart, name='cart'),
    path('cart/add_item/<int:item_id>',views.add_to_cart, name='add_to_cart'),
    path('cart/remove_item/<int:item_id>',views.remove_from_cart, name='remove_from_cart'),
    path('cart/update_item/<int:item_id>',views.update_cart_item, name='update_cart_item'),
    path('checkout',views.checkout, name='checkout'),
    path('order',views.order, name='order'),
    path('ecommerce/admin/login',views.admin_login, name='ecommerce_login'),
    path('ecommerce/admin/dashboard',views.admin_dashboard, name='ecommerce_dashboard'),
    path('ecommerce/admin/add_product',views.add_product, name='add_product'),
    path('ecommerce/admin/approve_product',views.approve_product, name='approve_product'),
    path('ecommerce/admin/review/product/<int:item_id>',views.review_product, name='review_product'),

]