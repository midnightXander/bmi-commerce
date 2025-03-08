from django.contrib import admin
from .models import *

admin.site.register(Item)
admin.site.register(ItemImage)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Message)

