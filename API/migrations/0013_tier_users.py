# Generated by Django 4.0.4 on 2022-05-13 20:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('API', '0012_alter_imagemodel_image_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='tier',
            name='users',
            field=models.ForeignKey(null=True, on_delete=models.SET(None), to=settings.AUTH_USER_MODEL),
        ),
    ]
