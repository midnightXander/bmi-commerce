# Generated by Django 5.1.2 on 2024-10-18 14:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_item_image1_item_image2_item_image3_item_image4'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
