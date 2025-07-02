from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('',views.index, name='index'),
    path('tests',views.tests, name='tests'),
    path('<str:test_type>/<str:module>',views.module, name='module'),
    path('tests/courses/<str:slug>',views.course, name='course'),
] 