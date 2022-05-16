# Generated by Django 4.0.4 on 2022-05-08 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_image_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='size',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tier',
            name='thumbnails',
            field=models.ManyToManyField(blank=True, to='API.thumbnail'),
        ),
    ]