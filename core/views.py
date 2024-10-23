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
import uuid



def get_session_key(request):
    session_key = request.session.session_key

    # if not session_key:
    #     return uuid.uuid4()
    return session_key
    


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
        'status': 'Approuvé' if item.approved else 'En attente',
        "provider": {
            "label": item.provider.label,
            "id": item.provider.id,
            "name": item.provider.user.username,
            "product_type": item.provider.product_type,
            "phone_number": item.provider.phone_number,
        }
    }  

def _provider_data(provider:Provider):
    return {
        'id': provider.id,
        'name': provider.name,
        'email': provider.user.email,
        'city': 'None',
        'country': provider.country,
        'status': 'Actif',
        'label':provider.label,
    }

def index(request):
    print(request.session.session_key)
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

def _get_cart_items(cart:Cart):
    cart_items = cart.items.all()
    for item in cart_items:
        parsed_item = item_data(item)
        cart_items_data = []
        cart_items = cart.items.all()
        parsed_item['quantity'] = CartItem.objects.get(item = item,cart = cart).quantity
        cart_items_data.append(parsed_item)

    return cart_items_data


def add_to_cart(request, item_id):
    item = Item.objects.get(id = item_id)
    session_key = get_session_key(request)

    if request.method == 'POST':
        #PUT A TRY CATCH INSTEAD
        if session_key:
            cart,created = Cart.objects.get_or_create(cart_key = session_key)
            if item in cart.items.all():
                return JsonResponse({'status':'failure', 'message':'Le produit est deja dans votre panier'})
            
            cart.items.add(item)
            cart.save()
            return JsonResponse({'status':'success', 'message':'Ajouté a votre panier'})
        else:
            return JsonResponse({'status':'failure', 'message':"Le produit n'a pas été ajouté a votre panier"})
def remove_from_cart(request, item_id):
    item = Item.objects.get(id = item_id)
    session_key = get_session_key(request)

    if request.method == 'POST':
        cart = Cart.objects.get(cart_key = session_key)
        if item not in cart.items.all():
            return JsonResponse({'status':'failure', 'message':"Le produit n'est pas dans votre panier"})
        
        cart.items.remove(item)
        cart.save()

        cart_items_data = []
        cart_items = cart.items.all()
        for item in cart_items:
            parsed_item = item_data(item)
            parsed_item['quantity'] = CartItem.objects.get(item = item,cart = cart).quantity
            cart_items_data.append(parsed_item)

        return JsonResponse({'status':'success', 'message':'Retiré de votre panier', 'items':cart_items_data})    

def update_cart_item(request, item_id):
    item = Item.objects.get(id = item_id)
    session_key = get_session_key(request)

    if request.method == 'POST':
        cart = Cart.objects.get(cart_key = session_key)
        if item not in cart.items.all():
            return JsonResponse({'status':'failure', 'message':"Le produit n'est pas dans votre panier"})
        
        change = request.POST['change']
        change = int(change)

        cart_item = CartItem.objects.get(item = item,cart = cart)
        
        cart_item.quantity += change
        
        if cart_item.quantity <=0:
            "remove item from cart" 
            cart_item.delete()
        else:
            cart_item.save()    

        cart.save()

        cart_items_data = []
        cart_items = cart.items.all()
        
        for item in cart_items:
            parsed_item = item_data(item)
            parsed_item['quantity'] = CartItem.objects.get(item = item,cart = cart).quantity
            cart_items_data.append(parsed_item)

        return JsonResponse({'status':'success', 'message':'updated', 'items':cart_items_data})    


def cart(request):
    session_key = get_session_key(request)
    cart,created = Cart.objects.get_or_create(cart_key = session_key)

    cart_items_data = []
    cart_items = cart.items.all()
    for item in cart_items:
        parsed_item = item_data(item)
        parsed_item['quantity'] = CartItem.objects.get(item = item,cart = cart).quantity
        cart_items_data.append(parsed_item)

    return render(request,"core/cart.html", {
        'products':cart_items_data,
    })

def checkout(request):
    session_key = get_session_key(request)
    cart = Cart.objects.get(cart_key = session_key)

    return render(request,"core/checkout.html", {
        'products':_get_cart_items(cart)
    })

def profile(request):
    
    provider = get_partner(request)
    
    return render(request,"core/profile.html", {
        "provider": provider,
    })




def admin_login(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.get(email=email)
             
        except:
            messages.error(request,"Informations incorrect")
            return HttpResponseRedirect(reverse("core:ecommerce_login")) 
        
        company = Provider.objects.filter(label = 'company', user = user )
        if not company.exists():
            messages.error(request,"Ce compte n'est pas administrateur BMI")
            return HttpResponseRedirect(reverse("core:ecommerce_login")) 
        
        user_auth = auth.authenticate(username=user.username,password=password)
        if user_auth is not None:
            auth.login(request,user_auth)
            return HttpResponseRedirect(reverse("core:ecommerce_dashboard"))
        else:
            messages.error(request,"Mot de passe incorrect")


        return HttpResponseRedirect(reverse("core:ecommerce_login"))
    return render(request,"core/login.html")

@login_required
def admin_dashboard(request):
    partner_products = Item.objects.filter(provider__label = 'partners')
    company_products = Item.objects.filter(provider__label = 'company')
    partner_products_data = []
    company_products_data = []
    for product in partner_products:
        partner_products_data.append(item_data(product))


    for product in company_products:
        company_products_data.append(item_data(product))

    partners  = Provider.objects.filter(label = 'partners')
    partners_data = []
    for partner in partners:
        partners_data.append(_provider_data(partner))    

    
    

    if request.method == 'POST':
        pass

    return render(request,"core/admin.html",{
        'partners' : partners_data, 
        'partner_products': partner_products_data,
        'company_products': company_products_data,

    })
@login_required
def add_product(request):
    if request.method == 'POST':
        pass
    
    return render(request, "core/add_product.html")