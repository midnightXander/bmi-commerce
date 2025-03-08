from rest_framework import serializers
from core.models import Item,Profile
from partner.models import Provider
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        print(validated_data)
        # user = User(
        #     email = validated_data['email'],
        #     username = validated_data['username']
        # )
        # user.set_password(validated_data['password'])
        #user.save()



        return user    

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'phone']

    def update(self, instance, validated_data):
        print("validated: ", validated_data)
        user_data:dict = validated_data.pop('user')    
        user:User = instance.user

        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        
        user.username = user_data.get('username', user.username)
        user.save()

        return instance

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




 


