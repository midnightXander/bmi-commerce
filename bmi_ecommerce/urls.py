"""
URL configuration for bmi_ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
#from customJwt import customTokenObtainPairView
#import customJwt


#OBTAINING TOKENS LOGIN with EMAIL
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
    

    def validate(self, attrs):

        try:
            user = User.objects.get(email = attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')    

        return super().validate(attrs)

class customTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenPairSerializer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls', namespace='core')),
    path('partner/',include('partner.urls', namespace='partner')),
    path('api/', include('api.urls', namespace='api')),

    #restframework auth
    path('api/token/', customTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),

    #api-auth
    path('auth', include('rest_framework.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

