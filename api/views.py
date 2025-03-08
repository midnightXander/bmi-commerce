from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.views import APIView 
from core.models import *
from .serializers import *
from django.contrib.auth.models import User



@csrf_exempt
def all_item_list(request, format=None):

    """
    List all products
    """

    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        #return Response(serializer.data)
        return JsonResponse(serializer.data, safe = False)
    elif request.method == 'PUT':
        """Edit a product"""
        #check user for eligibility
        pass

    elif request.method == 'DELETE':
        #check user for eligibility
        pass    

@api_view(['GET', 'PUT', 'DELETE'])
def item(request, pk,):
    """
    Retrieve a product 
    """
    
    try:
        item = Item.objects.get(pk = pk)
    except Item.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    

    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ItemSerializer(Item, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_user(request, email:str):
    """Get the user from email"""
    #user = request.user

    try:
        user = User.objects.get(email = email.strip())
        serializer = UserSerializer(user)
    except User.DoesNotExist:
        raise Http404
    
    return Response(serializer.data)

class CompanyItemList(APIView):
    """
    List Company products or create a new one 
    """

    def get(self, request, format=None):
        items = Item.objects.filter(provider__label = 'company')
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data) 
    
    def post(self, request, format= None):
        serializer = ItemSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class ProviderList(APIView):
    """
    List all product providers(partners)
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        providers = Provider.objects.all()
        serializer = ProviderSerializer(providers, many=True)
        return Response(serializer.data)
    

    
class ProviderDetail(APIView):
    """
    Retrieve a single partner
    """    

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_provider(self,pk):
        try:
            return Provider.objects.get(pk = pk)
        except Provider.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        provider = self.get_provider(pk)
        serializer = ProviderSerializer(provider)
        return Response(serializer.data)        


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Profile.objects.create(user = user)
        


class ProfileList(APIView):

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


    def get(self, request, format = None):
        profiles = Profile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = UserProfileSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileDetail(APIView):
    
    def get_profile(self, email):
        try:
            user = User.objects.get(email = email)
            profile  = Profile.objects.get(user = user )
            return profile

        except User.DoesNotExist or Profile.DoesNotExist:
            raise   Http404
        

    def put(self, request, email, format = None):
        profile = self.get_profile(email) 
        serializer = UserProfileSerializer(profile, data = request.data)
        print("data: ", request.data)
        print("profile: ", profile)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, email, format = None):
        profile = self.get_profile(email) 
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
     
     