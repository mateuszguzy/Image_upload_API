import datetime as dt
import json

from django.shortcuts import redirect
from dotenv import load_dotenv
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .additional_functions import validate_user, add_new_image, validate_parameters, encrypt_data, decrypt_data
from .models import ImageModel, UserModel
from .serializers import ImageSerializer

load_dotenv()


# ViewSet used on '' and 'images/' urls
class ImageViewSet(viewsets.ModelViewSet):
    """
    Default ViewSet listing all images uploaded by logged user.
    """
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    # overwriting default queryset, listing only images assigned to logged user
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user).order_by("image_name")


@api_view(['GET'])
def image_view(request, image_name) -> json:
    """
    Allowing user to view previously uploaded image
    :param request:
    :param image_name:
    :return :
    """
    # validate if user provided correct or any at all credentials
    user_is_valid = validate_user(request.user)
    # when user is authorized extract wanted image from DB and redirect to image location
    if user_is_valid:
        queryset = ImageModel.objects.filter(image_name=image_name.lower(), user_id=request.user.id).first()
        if queryset:
            return redirect(f'static/API/{queryset}')
        return Response({'Invalid credentials or image name': 401})
    else:
        return Response({'Unauthorized access': 401})


@api_view(['POST'])
def add_new_image_view(request) -> json:
    """
    Allow to add new images to DB with POST request
    :param request:
    :return:
    """

    if request.method == 'POST':
        user_is_valid = validate_user(request.user)
        if user_is_valid:
            images = add_new_image(request=request)
            return Response({'Added': images})
        else:
            return Response({'Unauthorized access': 401})


@api_view(['GET'])
def temporary_link_generator(request, image_name, seconds) -> json:
    """
    Allows for authorized users to generate temporary link, giving access for non-registered users to
    given image for certain amount of time
    :param request:
    :param image_name:
    :param seconds:
    :return:
    """
    # validate if user provided correct or any at all credentials
    user_is_valid = validate_user(request.user)

    if not user_is_valid:
        return Response({'Invalid credentials': 401})
    else:
        # check if user has permission to generate temporary links
        can_generate_temp_links = UserModel.objects.filter(user_id=request.user.id).first().tier.expiring_links
        print(can_generate_temp_links)
        if can_generate_temp_links:
            # check if image for temporary link is available
            validated_parameters = validate_parameters(request=request, image_name=image_name.lower(), seconds=seconds)
            if validated_parameters:
                temporary_link = encrypt_data(image_name=image_name.lower(), seconds=seconds)
                return Response({'Temporary_link': temporary_link})
            else:
                return Response({'Image name or seconds value not valid': 400})
        else:
            return Response({'Cannot generate temporary link. Functionality is not a part of current tier': 401})


@api_view(['GET'])
def temporary_link_view(request, token) -> json:
    """
    Validate temporary link and if validation is passed show required image to user
    :param request:
    :param token:
    :return:
    """
    # decrypt data from URL
    expiration_date, image_name = decrypt_data(token=token)
    # check if link is expired
    current_date = str(dt.datetime.now())

    if expiration_date < current_date:
        return Response({'Link expired': 404})
    else:
        # redirect to image location (no need to validate if image is present in DB
        # because for now there is no DELETE functionality for users)
        image_name = ImageModel.objects.filter(image_name=image_name.lower()).first()
        image_path = f'static/API/{str(image_name)}'
        return redirect(f'/{image_path}')
