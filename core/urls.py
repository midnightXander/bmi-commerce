from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.index, name='index'),
    path('upload', views.upload,name = 'upload'),
    path('message', views.message,name = 'message'),

    path('travel-pro',views.travelpro, name='about'),
    path('clever-life',views.cleverlife, name='about'),
    path('business-consulting',views.consulting, name='about'),
    
    path('services',views.services, name='services'),
    path('realisations',views.work, name='work'),
    path('notre-equipe',views.team, name='team'),
    path('produits',views.products, name='products'),
    path('produits/<str:ref>',views.product, name='product'),
    path('reviews/<int:product_id>',views.reviews, name='review'),
    path('profile',views.profile, name='profile'),
    path('contact',views.contact, name='contact'),
    path('blogposts',views.blog, name='blog'),
    path('blogposts/<int:post_id>',views.blog_post, name='blogPost'),
    path('download',views.app_page, name='download_app'),
    path('cart',views.cart, name='cart'),

    path('cart/add_item/<int:item_id>',views.add_to_cart, name='add_to_cart'),
    path('cart/remove_item/<int:item_id>',views.remove_from_cart, name='remove_from_cart'),
    path('cart/update_item/<int:item_id>',views.update_cart_item, name='update_cart_item'),
    path('checkout',views.checkout, name='checkout'),
    path('order',views.order, name='order'),
    path('ecommerce/admin/login',views.admin_login, name='ecommerce_login'),
    path('ecommerce/admin/dashboard',views.admin_dashboard, name='ecommerce_dashboard'),
    path('ecommerce/admin/add_product',views.add_product, name='add_product'),
    path('ecommerce/admin/posts/add',views.add_blog_post, name='add_post'),
    path('ecommerce/admin/approve_product',views.approve_product, name='approve_product'),
    path('ecommerce/admin/review/product/<int:item_id>',views.review_product, name='review_product'),

]