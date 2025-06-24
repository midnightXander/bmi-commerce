from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('languages',views.index, name='index'),
] 