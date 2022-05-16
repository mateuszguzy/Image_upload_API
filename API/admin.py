from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Tier, Thumbnail, ImageModel, UserModel

# Register your models here.
admin.site.register(Tier)
admin.site.register(Thumbnail)
admin.site.register(ImageModel)
admin.site.register(UserModel)
admin.site.unregister(Group)
