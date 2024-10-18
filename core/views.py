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


def index(request):
    return render(request,"core/index.html")

def products(request):
    return render(request,"core/products.html")

def services(request):
    return render(request, "core/services.html")

def product(request, id):
    return render(request,"core/product.html")

def profile(request):
    
    provider = get_partner(request)
    
    return render(request,"core/profile.html", {
        "provider": provider,
    })



