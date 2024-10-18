from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
import uuid
from partner.models import Provider
from django.utils import timezone

class ItemColor(models.Model):
    """color for an item"""
    pass



class Item(models.Model):
    
    name = models.CharField(max_length=50)
    ref = models.CharField(max_length=20)
    description = models.TextField()
    price = models.IntegerField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to = "items/images/", blank=True)
    image2 = models.ImageField(upload_to = "items/images/", null=True)
    image3 = models.ImageField(upload_to = "items/images/", null=True)
    image4 = models.ImageField(upload_to = "items/images/", null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name}: {self.provider.name}"
    
class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = "items/images/")

    def __str__(self):
        return f"{self.item.name}"    

class Client(models.Model): 
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.user}"


class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    value = models.IntegerField()
    date_added = models.DateTimeField()

    def __str__(self):
        return f"{self.value}"