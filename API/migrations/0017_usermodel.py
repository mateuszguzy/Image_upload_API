# Generated by Django 4.0.4 on 2022-05-13 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0016_delete_usermodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('tier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='API.tier')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
