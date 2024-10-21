from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User,auth
from django.urls import reverse
from django.http import HttpResponseRedirect,JsonResponse,Http404
from django.contrib.auth import logout,login,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from partner.models import Provider
import uuid
from django.db.models import Q,QuerySet
import re
import datetime
import core.views as core_views
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from partner.views import get_partner

def item_data(item:Item):
    return {
        "id": item.id,
        "name": item.name,
        "ref": item.ref,
        "description": item.description,
        "price": item.price,
        "image1": item.image1.url,
        "image2": item.image2.url if item.image2 else None,
        "image3": item.image3.url if item.image3 else None,
        "image4": item.image4.url if item.image4 else None,
        "provider": {
            "label": "partners",
            "id": item.provider.id,
            "name": item.provider.user.username,
            "product_type": item.provider.product_type,
            "phone_number": item.provider.phone_number,
        }
    }  

def index(request):
    return render(request,"core/index.html")

def products(request):
    products = []
    for item in Item.objects.all().order_by('-date_added'):
        products.append(item_data(item))

    return render(request,"core/products.html", {
        "products": products,
    })

def services(request):
    return render(request, "core/services.html")

def product(request, ref):
    item = get_object_or_404(Item, ref = ref)
    
    return render(request,"core/product.html", {
        'product': item_data(item)
    })

def profile(request):
    
    provider = get_partner(request)
    
    return render(request,"core/profile.html", {
        "provider": provider,
    })



