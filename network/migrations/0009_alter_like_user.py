# Generated by Django 3.2.6 on 2021-10-09 09:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_auto_20211008_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ManyToManyField(blank=True, default=None, to=settings.AUTH_USER_MODEL),
        ),
    ]