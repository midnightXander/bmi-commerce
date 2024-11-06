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
from core.utility import *
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from partner.views import get_partner
import uuid
from django.core.files.storage import FileSystemStorage
import yagmail

def get_session_key(request):
    session = request.session
    session_key = session.get('cart_key')
    if session_key:
        return session_key
    else:
        session['cart_key'] = str(uuid.uuid4())
        session_key = session['cart_key']
    
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
            'city': item.provider.city
        }
    }  

def _order_item_data(order:Order,cartitem:CartItem):
    _item_data = item_data(cartitem.item)
    _item_data['quantity'] = cartitem.quantity
    _item_data['total'] = cartitem.quantity * cartitem.item.price
    return {
        "order_id": order.id, 
        "timestamp": order.date_ordered,
        "customer":{
            "name": f"{order.name} {order.surname}",
            "address": order.adress,
            "email": order.email,
            "city":order.city,
        },
        "item":_item_data,

    }


def _provider_data(provider:Provider):
    return {
        'id': provider.id,
        'name': provider.name,
        'email': provider.user.email,
        'city': provider.city,
        'status': 'Actif',
        'label':provider.label,
    }

def index(request):
    
    return render(request,"core/index.html")

def upload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        fs = FileSystemStorage()

        try:
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
            print(file_url)
            return render(request, 'core/image_url.html', {
                'file_url': file_url,
            })
        except Exception as e:
            print(f'Error uploading to s3: {e}')
    return render(request, 'core/upload.html')

def products(request):
    products = []
    for item in Item.objects.all().order_by('-date_added'):
        products.append(item_data(item))
    
    return render(request,"core/products.html", {
        "products": products,
    })

def services(request):
    return render(request, "core/services.html")

def team(request):
    return render(request, "core/team.html")

def product(request, ref):
    item = get_object_or_404(Item, ref = ref)
   
    return render(request,"core/product.html", {
        'product': item_data(item)
    })

def _get_cart_items(cart:Cart):
    cart_items = cart.items.all()
    cart_items_data = []
    for item in cart_items:
        parsed_item = item_data(item)
       
        cart_items = cart.items.all()
        parsed_item['quantity'] = CartItem.objects.get(item = item,cart = cart).quantity
        cart_items_data.append(parsed_item)

    return cart_items_data


def add_to_cart(request, item_id):
    item = Item.objects.get(id = item_id)
    session_key = get_session_key(request)

    if request.method == 'POST':
        #PUT A TRY CATCH INSTEAD
        
        cart,created = Cart.objects.get_or_create(cart_key = session_key)
        if item in cart.items.all():
            return JsonResponse({'status':'failure', 'message':'Le produit est deja dans votre panier'})
        
        cart.items.add(item)
        cart.save()
        return JsonResponse({'status':'success', 'message':'Ajouté a votre panier'})
        # else:
        #     return JsonResponse({'status':'failure', 'message':"Le produit n'a pas été ajouté a votre panier"})
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
    if len(cart.items.all()) == 0:
        return render(request,'core/empty_cart.html')


    return render(request,"core/checkout.html", {
        'cart_key': cart.cart_key,
        'products': _get_cart_items(cart)
    })

def profile(request):
    
    provider = get_partner(request)
    orders = []
    all_orders = Order.objects.all().order_by('-date_ordered')
    if provider:
        provider_items = Item.objects.filter(provider = provider) 
        for order in all_orders:
            cartitems = CartItem.objects.filter(cart = order.cart) 
            
            for cartitem in cartitems:
                print(cartitem.item.provider)
                print(provider)
                if cartitem.item.provider == provider:
                    order_data = _order_item_data(order, cartitem)
                    orders.append(order_data)

    
    return render(request,"core/profile.html", {
        "provider": provider,
        "orders": orders[:10]

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


def order(request):
    
    if request.method == 'POST':
        cart_key = request.POST['cart_key']
        cart = Cart.objects.get(cart_key = cart_key)
        name = request.POST['firstName']
        surname = request.POST['lastName']
        email = request.POST['email']
        phone = request.POST['phone']
        city = request.POST['city']
        adress = request.POST['address']

        new_order = Order.objects.create(
            name = name,
            email = email,
            surname = surname,
            phone = phone,
            adress = adress,
            city = city,
            cart = cart,
        )

        #NOTIFY PROVIDER(S) for each item in cart
        items = CartItem.objects.filter(cart=cart)
        for item in items:
            send_order_email(item.item.provider.user.email, item, {
                "name": f"{name} {surname}",
                "email": email,
                "phone": phone,
                "city":city, 
                "adress":adress
            })

        new_order.save()
        message = {
            'status': 'success',
            'content': 'Votre commande a été enregistré, le fournisseur va vous contacter pour valider la commande'
        }
        return render(request,'core/order_finished.html', {
            'message': message
        })
