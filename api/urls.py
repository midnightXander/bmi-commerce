from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

urlpatterns = [
    path('items', views.all_item_list,  name='items'),
    path('items/<int:pk>', views.item,  name='item'),
    path('items/company', views.CompanyItemList.as_view()),
    
    #providers
    path('providers', views.ProviderList.as_view()),
    path('providers/<int:pk>', views.ProviderDetail.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)