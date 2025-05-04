from django.urls import path
from . import views

app_name = 'partner'

urlpatterns = [
    path('register',views.register, name='register'),
    path('login',views.login, name='login'),
    path('logout',views.logout_view, name='logout'),
    path('products/<int:provider_id>',views.get_provider_items, name='products'),
    path('products/delete/<int:product_id>',views.delete_product, name='delete_product'),
    path('products/edit/<int:product_id>',views.edit_product, name='edit_product'),
    path('products/add',views.add_product, name='add_product'),
    path('accounts/password/recover', views.password_recover, name = 'password_recover'),
    path('accounts/password/reset', views.password_reset, name = 'password_reset'),

    #partners pages
    path('clever-life', views.cleverlife, name = 'growth_hair_oil'),
    path('page/<str:slug>', views.partner_page, name = 'partner_page'),
    

]
