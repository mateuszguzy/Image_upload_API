import datetime as dt
import os

from PIL import Image
from cryptography.fernet import Fernet

from .models import ImageModel, UserModel


def validate_user(user) -> bool:
    """
    Check if user provided correct or any credentials.
    :param user:
    :return:
    """
    if str(user) == 'AnonymousUser':
        return False
    return True


# adjust showed images to just that uploaded by currently logged user
def get_queryset(request) -> dict:
    """
    Get currently existing images data assigned to authorized user from DB
    :param request:
    :return:
    """
    queryset = ImageModel.objects.all()
    user = request.user
    return queryset.filter(user=user)


def check_for_duplicates(user, image_name) -> bool:
    """
    Check DB for image with name exactly the same as currently upladed one
    :param user:
    :param image_name:
    :return:
    """
    for image in ImageModel.objects.filter(image_name=image_name):
        if image.user_id == user.id:
            return False
    return True


def save_new_image(request, user, image_size, image_name) -> str:
    """
    Transform image to required size and save, assigning it to authorized user
    :param request:
    :param user:
    :param image_size:
    :param image_name:
    :return:
    """
    # check DB if authorized user has previously uploaded image with the same name
    no_duplicates = check_for_duplicates(user, str(image_name))
    if no_duplicates:
        # transform image to required size
        with Image.open(request.data['image_name']) as img:
            if image_size == 'original':
                image_size = img.size[1]
            img.thumbnail(size=(img.size[0], image_size))
            # save image in STATIC files folder
            save_path = f'API/static/API/{str(image_name)}'
            img.save(fp=save_path)
            # add image data to DB
            new_image = ImageModel(user_id=user.id, size=image_size, image_name=image_name)
            new_image.save()
            return image_name.lower()
    # if image with current name (and size) exists return such information for user
    # in case user changes Tier, after uploading the same file, only new sizes will be added)
    return f'Image: {image_name} already in database.'


def add_new_image(request) -> list:
    """
    Create thumbnails of uploaded image. That many and with that sizes, which user has in current Tier
    :param request:
    :return:
    """
    # list of images added to DB later returned in JSON response
    images = list()
    # list of accepted file extensions
    possible_extensions = ['jpg', 'png']
    # from current user data extract Tier information
    current_tier = UserModel.objects.filter(user_id=request.user.id).first().tier
    user = request.user
    # from provided image extract extension and check if it's valid
    extension = str(request.data.get('image_name')).split('.')[1].lower()
    sizes_to_save = list()
    if extension in possible_extensions:
        if current_tier.original_image:
            sizes_to_save.append('original')
        for thumbnail in current_tier.thumbnails.all():
            sizes_to_save.append(thumbnail.size)
    # for every thumbnail size available in current user tier, transform and save image
    for image_size in sizes_to_save:
        image_name = f"{user}_{str(request.data.get('image_name')).split('.')[0]}_{image_size}.{extension}".lower()
        saved_image = save_new_image(request=request, user=user, image_size=image_size, image_name=image_name)
        images.append(saved_image)
    return images


def validate_parameters(request, image_name, seconds) -> bool:
    """
    Check if provided by user parameters are valid: image is present in DB and number of seconds is
    within a required range
    :param request:
    :param image_name:
    :param seconds:
    :return:
    """
    # check if provided image_name is present in DB for given user
    if ImageModel.objects.filter(image_name=image_name) and \
            ImageModel.objects.filter(image_name=image_name).first().user_id == request.user.id:
        # check if user provided correct number of seconds for link to expire
        if 30 <= seconds <= 30000:
            return True
    return False


def encrypt_data(image_name, seconds) -> str:
    """
    Encrypt image name and number of seconds for temporary link to expire into token passed into URL
    :param image_name:
    :param seconds:
    :return:
    """
    # get encryption token from .env file
    key = os.environ.get('SECRET')
    # calculate link expiration time
    time_to_expire = dt.timedelta(seconds=seconds)
    current_date = dt.datetime.now()
    expiration_time = (current_date + time_to_expire)
    # encrypt expiration time and image name, into token which will be provided passed URL
    f = Fernet(key)
    text_to_encryption = bytes(f'{expiration_time}<>{image_name}', 'utf-8')
    token = f.encrypt(text_to_encryption)
    # combine token with base urs for full link
    temporary_link = os.environ.get('TMP_LINKS_URL') + str(token)[2:-1]
    return temporary_link


def decrypt_data(token) -> list:
    """
    Decrypt image name and number of seconds for temporary link to expire to check if link is still valid
    :param token:
    :return:
    """
    # convert token from string to bytes
    token_in_bytes = bytes(token, 'utf-8')
    key = os.environ.get('SECRET')
    f = Fernet(key)
    decrypted_string = f.decrypt(token_in_bytes)
    # return image name and seconds value
    return str(decrypted_string)[2:-1].split('<>')
