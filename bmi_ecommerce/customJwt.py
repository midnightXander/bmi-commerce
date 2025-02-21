from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
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
    
