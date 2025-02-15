from rest_framework import serializers
from core.models import Item
from partner.models import Provider
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
        ]

class ItemSerializer(serializers.ModelSerializer):
    #provider = ProviderSerializer(read_only = True)
    provider = serializers.ReadOnlyField(source = 'provider.name')
    #additional = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = [
            'id', 'name', 'ref', 'price', 'description',
            'image1','image2','image3', 'image4','date_added',
            'provider',
            #additional
            ]

    def get_additional_field(self, obj):
        return 1   


class ProviderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    items = serializers.PrimaryKeyRelatedField(many=True, queryset = Item.objects.all())
    #items = ItemSerializer(many=True, read_only = True)
    class Meta:
        model = Provider
        fields = [
            'id', 'user', 'name', 'phone_number', 'product_type', 'city',
            'label', 'items'
        ]




 


