# Generated by Django 4.0.4 on 2022-05-08 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tier',
            name='thumbnails',
        ),
        migrations.AddField(
            model_name='tier',
            name='thumbnails',
            field=models.ManyToManyField(to='API.thumbnail'),
        ),
    ]