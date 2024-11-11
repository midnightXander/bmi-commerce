from .models import Item,CartItem
import yagmail
from dotenv import load_dotenv
import os


load_dotenv()

def parse_id(number):
    if number < 10:
        return f"00{number}"
    elif number <= 100:
        return f"0{number}"
    else:
        return str(number)

def item_ref(item_name:str):
    n_items = len(Item.objects.all())
    decomposed = item_name.split()
    ref = ""
    for name in decomposed:
        ref += name[0]
    ref = ref.upper()

    number_id = parse_id(n_items+1)
    ref += f"-{number_id}"
    
    return ref

def send_new_product_email(item:Item):
    sender_adress = os.environ['BMI_EMAIL']
    _pwd = os.environ['EMAIL_PWD']
    contact_address = os.environ['CONTACT_EMAIL']
    html_content = f"""
        <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nouvau produit ajouté</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
<p>Un nouveau produit a été ajouté et a besoin d'etre validé:  {item}</p>
<p style="color: #666666; font-size: 16px; margin: 0 0 20px 0;">
{item.date_added},
</p>
<p style="color: #666666; font-size: 16px; margin: 0 0 20px 0;">
{item.provider.name},
</p>
<a  href='https://bmisolutions.org/ecommerce/admin/review/product/{item.id}'>Verifier le produit</a>
</body>
</html>
    
    """

    try:
        with yagmail.SMTP(sender_adress, _pwd) as yag:
            yag.send(
                to=contact_address,
                subject="Nouveau produit ajouté",
                contents=html_content
            )
            print(f"email sent to {contact_address}")
    except Exception as e:
        print(f"An error occured: {e}")

def send_order_email(email,cart_item:CartItem,customer_data:dict):
    
    sender_adress = os.environ['BMI_EMAIL']
    _pwd = os.environ['EMAIL_PWD']
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nouvelle commande</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
        <!-- Header -->
        <tr>
            <td style="padding: 30px 20px; text-align: center; background-color: #2563eb;">
                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Nouvelle Commande</h1>
            </td>
        </tr>

        <!-- Content -->
        <tr>
            <td style="padding: 30px 20px;">
                <p style="color: #666666; font-size: 16px; margin: 0 0 20px 0;">
                    {cart_item.item.provider.name},
                </p>
                <p style="color: #666666; font-size: 16px; margin: 0 0 20px 0;">
                    Vous avez reçu une commande pour un produit dans BMI:
                </p>

                <!-- Order Info -->
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
                    <p style="margin: 0 0 10px 0; color: #333333;">
                        <strong>Information client:</strong>
                        <strong>Nom: {customer_data['name']}</strong>
                        <strong>phone: {customer_data['phone']}</strong>
                        <strong>email: {customer_data['email']}</strong>
                        <strong>ville: {customer_data['city']}</strong>
                        <strong>adressse: {customer_data['adress']}</strong>
                    </p>
                    <p style="margin: 0 0 10px 0; color: #333333;">
                        <strong>Commande numero:</strong> 032{cart_item.cart.id}
                    </p>
                    <p style="margin: 0 0 10px 0; color: #333333;">
                        <strong>Produit:</strong> {cart_item.item.name}-{cart_item.item.ref}
                    </p>
                    <p style="margin: 0 0 10px 0; color: #333333;">
                        <strong>Quantité:</strong> {cart_item.quantity}
                    </p>
                    <p style="margin: 0; color: #333333;">
                        <strong>Montant Total:</strong> {cart_item.quantity*cart_item.item.price} FCFA 
                    </p>
                </div>

                <!-- CTA Button -->
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin: 30px 0;">
                    <tr>
                        <td align="center">
                        <a href="https://bmisolutions.org/profile" style = "color: red; padding:12px 30px border: 1px solid white; border-radius: 5px;">
                                Details
                        </a>
                            <a href="https://bmisolutions.org/profile" style="display: inline-block; 
                                      padding: 12px 30px; 
                                      background-color: #2563eb; 
                                      color: #ffffff; 
                                      text-decoration: none; 
                                      border-radius: 5px; 
                                      font-weight: bold;">
                                Details
                            </a>
                            
                        </td>
                    </tr>
                </table>

                <p style="color: #666666; font-size: 14px; margin: 0;">
                    Si vous avez des questions, ecrivez a l'equipe a l'email contact@bmisolutions.org
                </p>
            </td>
        </tr>

        <!-- Footer -->
        <tr>
            <td style="padding: 20px; background-color: #f8f9fa; text-align: center;">
                <p style="color: #666666; font-size: 12px; margin: 0;">
                    © 2024 BMI. Tous droits reservé.
                </p>
            </td>
        </tr>
    </table>
</body>
</html>
        
"""
    try:
        with yagmail.SMTP(sender_adress, _pwd) as yag:
            yag.send(
                to=email,
                subject="Nouvelle Commande",
                contents=html_content
            )
            print(f"email sent to {email}")
    except Exception as e:
        print(f"An error occured: {e}")
