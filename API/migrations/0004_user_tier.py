# Generated by Django 4.0.4 on 2022-05-08 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_tier_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='API.tier'),
            preserve_default=False,
        ),
    ]
