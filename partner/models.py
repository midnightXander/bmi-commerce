from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
import uuid


class Provider(models.Model):
    name = models.CharField(max_length=70)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    phone_number = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    product_type = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.country}: {self.user.username}"