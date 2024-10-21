from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User,auth
from django.urls import reverse
from django.http import HttpResponseRedirect,JsonResponse,Http404
from django.contrib.auth import logout,login,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from core.models import *
import uuid
from django.db.models import Q,QuerySet
import re
import datetime
import core.views as core_views
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from core.utility import *

def get_partner(request):
    try:
        provider = Provider.objects.get(user = request.user)
    except Exception as e:
        provider = None

    return provider    


def register(request, referall_code = ""):
    if request.method == "POST":
        name = request.POST["companyName"]
        email = request.POST['email']
        country = request.POST['country']
        product_type = request.POST['product_type']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        

        if(password1 == password2):
            if User.objects.filter(email=email).exists():
                messages.info(request,"L'email est déja pris")
                return HttpResponseRedirect(reverse("core:profile"))
            elif User.objects.filter(username=name).exists():
                messages.error(request,"une entreprise avec ce nom a déja été enrigistrer")
                return HttpResponseRedirect(reverse("core:profile"))
            else:        
                new_user = User.objects.create_user(username=name,email=email,password=password1)
                new_partner = Provider.objects.create(

                    user = new_user,
                    product_type = product_type,
                    phone_number = phone_number,
                    country = country,
                    )
                
                user_auth = auth.authenticate(username = name,password=password1)
                auth.login(request,user_auth)
                new_user.save()
                new_partner.save()

                # try:
                #     # sendWelcomeEmail(new_user.email)
                #     pass
                # except Exception as e:
                #     print(f"could not send email: {e}")    

        else:
            messages.error(request,"Les mots de passes ne sont pas identiques")    
            
    return HttpResponseRedirect(reverse("core:profile"))


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,"Aucun compte avec ces informations")
            return HttpResponseRedirect(reverse("core:profile")) 
        
        user_auth = auth.authenticate(username=user.username,password=password)
        if user_auth is not None:
            auth.login(request,user_auth)
            #return HttpResponseRedirect(reverse("core:profile"))
        else:
            messages.error(request,"Incorrect Password")
            


    return HttpResponseRedirect(reverse("core:profile"))

def add_product(request):
    provider = get_partner(request)
    name = request.POST['productName']
    description = request.POST['productDescription']
    price = request.POST['productPrice']
    image1 = request.FILES['image1']
    image2 = request.FILES.get('image2')
    image3 = request.FILES.get('image3')
    image4 = request.FILES.get('image4')
    ref = item_ref(name)
    new_product = Item.objects.create(
        provider = provider,
        name = name,
        ref = ref,
        description = description,
        price = price,
        image1 = image1,
        image2 = image2,
        image3 = image3,
        image4 = image4,
    )

    new_product.save()
        

    return HttpResponseRedirect(reverse("core:profile"))


  

def get_provider_items(request,provider_id):
    provider = get_object_or_404(Provider, id = provider_id)
    items = Item.objects.filter(provider = provider).order_by('-date_added')
    items_data = []

    for item in items:
        data = core_views.item_data(item)
        items_data.append(data)

    return JsonResponse({"items":items_data, "status":'success'})    





