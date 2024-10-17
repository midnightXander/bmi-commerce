from django.urls import path
from . import views

app_name = 'moderator'

urlpatterns = [
    path('',views.index, name='index'),
    path('services',views.services, name='services'),
    path('produits',views.products, name='products'),
    path('produits/<int:id>',views.product, name='product'),

]