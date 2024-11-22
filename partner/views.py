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
import boto3
from dotenv import load_dotenv
import string,random,secrets

load_dotenv()

s3 = boto3.client( 's3',
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name = 'eu-north-1'

)

#deleted

def get_partner(request):
    try:
        provider = Provider.objects.get(user = request.user)
    except Exception as e:
        provider = None

    return provider    

def generate_reset_key():
    """Function to generate a key that is used to  let users reset their passwords for a certain time"""
    key = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    return key

def password_recover(request):
    if request.method == "POST":
        user_data = request.POST['user_data']
        
        user = User.objects.filter(Q(username = user_data) | Q(email = user_data)) 
        if len(user)>0:
            
            #send email with link
            user = user[0]
            user_email = user.email
            try:
                provider = Provider.objects.get(user = user)
                code = PasswordRecoveryCode.objects.create(key = generate_reset_key(), provider = provider)
                link = f"https://bmisolutions.org/partner/accounts/password/reset?k={code.key}"
                send_reset_password_link(link, user_email)
                code.save()
                
                #sendResetPasswordLink(user_email)                
                messages.success(request, f"Un lien a été  envoyé a {user_email}")
            except Exception as e:
                print(f"Error in sending link to {user_email}: {e}") 
                messages.error(request, "Une erreur s'est produite pendant l'envoie du mail")   
        else:
            messages.error(request, "Aucun Partenaire n'a été trouvé avec ce nom ou email")

    return render(request, "partner/accounts/password_recover.html")

def password_reset(request):
    
    key = request.GET.get('k')
    
    code = get_object_or_404(PasswordRecoveryCode,key = key)
    
    #get the difference in days since created and delete if greater than or equal to 1
    now = timezone.now()
    difference = now - code.date_created

    days = difference.days
    if days >=1:
        code.delete()
        print("deleted code")
        raise Http404
        # validity = {
        #     'value': False,
        #     'message':"ce lien n'est plus valid"
        # }
    if key:
        provider = code.provider
        user = provider.user
        if request.method == 'POST':
            new_password = request.POST['new_password']
            new_password2 = request.POST['new_password2']

            if new_password == new_password2:
                if len(new_password) < 8:
                    messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères')
                    return redirect(f'/partner/accounts/password/reset?k={key}')
                
                else:    
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Votre Mot de passe a été changé avec succès")
                    code.delete()

                    return redirect('/profile')
            else:
                messages.error(request, 'Les mot de passe ne sont pas identiques')
                return redirect(f'/partner/accounts/password/reset?k={key}')


        return render(request, "partner/accounts/password_reset.html",{
            "validity":True,
            'key': key,
            
        })
    else:
        print("No key")
        raise Http404


def register(request, referall_code = ""):
    if request.method == "POST":
        print('creating account...')
        name = request.POST["companyName"]
        email = request.POST['email']
        city = request.POST['city']
        product_type = request.POST['product_type']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        

        if(password1 == password2):
            if User.objects.filter(email=email).exists():
                messages.info(request,"un compte avec cet email existe déja")
                print('email exist deja...')
                return HttpResponseRedirect(reverse("core:profile"))
            elif User.objects.filter(username=name).exists():
                messages.error(request,"un partenaire avec ce nom a déja été enrigistrer")
                print('name in use...')
                return HttpResponseRedirect(reverse("core:profile"))
            else:        
                new_user = User.objects.create_user(username=name,email=email,password=password1)
                new_partner = Provider.objects.create(
                    name = name,
                    user = new_user,
                    product_type = product_type,
                    phone_number = phone_number,
                    city = city,
                    label = 'partners' 
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
            print("passwords don't match...")
    return HttpResponseRedirect(reverse("core:profile"))


def login(request):

    if request.method == "POST":
        print('logging in...')
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,"Aucun compte avec ces informations")
            print('No account with these infos...')
            return HttpResponseRedirect(reverse("core:profile")) 
        
        user_auth = auth.authenticate(username=user.username,password=password)
        if user_auth is not None:
            auth.login(request,user_auth)
            #return HttpResponseRedirect(reverse("core:profile"))
        else:
            print('incorrect passwords...')
            messages.error(request,"Mot de passe incorrect")
            


    return HttpResponseRedirect(reverse("core:profile"))

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("core:index"))

def upload_image_to_s3(image):
    try:
        print(image)
        s3.upload_file(f'media/{image}', 'bmiecommercebucket', f'media/{image}')
        print('uploaded to s3')
    except Exception as e:
        print(f'error uploading file: {e}')    

def add_product(request):
    provider = get_partner(request)
    if request.method ==  "POST":
        print("getting info...")
        name = request.POST['productName']
        description = request.POST['productDescription']
        price = request.POST['productPrice']
        image1 = request.FILES.get('image1')
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
        print("stored info...")
    
        new_product.save()
        new_product.image1.name.split('/')[-1]

        upload_image_to_s3(new_product.image1)
        upload_image_to_s3(new_product.image2)
        

        # s3.upload_file(f'{new_product.image1}', 'bmiecommercebucket', f'media/{new_product.image1}')
        # s3.upload_file(f'{new_product.image2}', 'bmiecommercebucket', f'media/{new_product.image2}')
        
        if(image3):
            
            upload_image_to_s3(new_product.image3)

            #s3.upload_file(f'{new_product.image3}', 'bmiecommercebucket', f'media/{new_product.image3}')

        if(image4):
            pass
            upload_image_to_s3(new_product.image4)
            #s3.upload_file(f'{new_product.image4}', 'bmiecommercebucket', f'media/{new_product.image4}')

        if provider.label == 'company':
            new_product.approved = True
            new_product.save()
            return JsonResponse({'status': 'success','label':'company'}) 
        else:
            send_new_product_email(new_product)    
    
    return JsonResponse({'status': 'success'})


def edit_product(request, product_id):
    partner = get_partner(request)
    if partner and partner.user == request.user:
        product = get_object_or_404(Item, id = product_id)
    else:
        raise Http404    
    
    if request.method == 'POST':
        product.name = request.POST['productName']
        product.description = request.POST['productDescription']
        product.price = request.POST['productPrice']
        product.image1 = request.FILES['image1']
        product.image2 = request.FILES.get('image2')
        product.image3 = request.FILES.get('image3')
        # product.image4 = request.FILES.get('image4')
        
        provider = product.provider

        product.save()
        product.image1.name.split('/')[-1]
        s3.upload_file(f'{product.image1}', 'bmiecommercebucket', f'media/{product.image1}')
        s3.upload_file(f'{product.image2}', 'bmiecommercebucket', f'media/{product.image2}')
        
        if(product.image3):
            s3.upload_file(f'{product.image3}', 'bmiecommercebucket', f'media/{product.image3}')

        if(product.image4):
            s3.upload_file(f'{product.image4}', 'bmiecommercebucket', f'media/{product.image4}')

        if provider.label == 'company':
            return HttpResponseRedirect(reverse("core:ecommerce_dashboard"))     
        
        return HttpResponseRedirect(reverse("core:profile"))

    return render(request,"core/edit_product.html" ,{
        'item': core_views.item_data(product),
    })


def get_provider_items(request,provider_id):
    provider = get_object_or_404(Provider, id = provider_id)
    items = Item.objects.filter(provider = provider).order_by('-date_added')
    items_data = []

    for item in items:
        data = core_views.item_data(item)
        items_data.append(data)

    return JsonResponse({"items":items_data, "status":'success'})    


def delete_product(request, product_id):
    item = Item.objects.get(id = product_id)
    if request.method == "POST":
        item.delete()
        return JsonResponse({'status':'success','message':'Produit Supprimé'})
    return JsonResponse({'status':'error','message':'Bad request'})
    


