from API.models import ImageModel
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['image_name']
