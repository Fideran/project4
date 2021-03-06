# Generated by Django 3.2.6 on 2021-10-08 09:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_auto_20211008_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='network.post'),
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ManyToManyField(default=None, to=settings.AUTH_USER_MODEL),
        ),
    ]
