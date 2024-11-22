from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
import uuid

PROVIDER_LABELS = ['company', 'partners']




class Provider(models.Model):
    name = models.CharField(max_length=70)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    phone_number = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    product_type = models.CharField(max_length=60)
    label = models.CharField(max_length=30, choices=[
        (i,i) for i in PROVIDER_LABELS
    ], default='company')

    def __str__(self):
        return f"{self.city}: {self.name}"
    

class PasswordRecoveryCode(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return f"{self.provider}"     


class Subscription(models.Model):
    """This models represents the subscription tier in which the partner is"""
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    date_started = models.DateField(auto_now_add=True)
    #expiry_date = models.DateField()

    def __str__(self):
        return f"{self.provider} from {self.date_started.day}"