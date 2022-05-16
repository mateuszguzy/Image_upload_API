from django.db import models
from django.contrib.auth.admin import User


class Thumbnail(models.Model):
    size = models.IntegerField()

    def __str__(self):
        return f'{self.size}'


class Tier(models.Model):
    name = models.CharField(max_length=100, blank=False)
    expiring_links = models.BooleanField(blank=False)
    original_image = models.BooleanField(blank=False)
    thumbnails = models.ManyToManyField(Thumbnail, blank=True)

    def __str__(self):
        return f'{self.name}'


class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user}'


class ImageModel(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.IntegerField(blank=False)
    image_name = models.ImageField(blank=False)

    def __str__(self):
        return f'{self.image_name}'
