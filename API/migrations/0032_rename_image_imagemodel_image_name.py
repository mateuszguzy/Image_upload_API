# Generated by Django 4.0.4 on 2022-05-15 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0031_alter_imagemodel_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagemodel',
            old_name='image',
            new_name='image_name',
        ),
    ]