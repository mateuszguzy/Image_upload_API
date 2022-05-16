"""Image_upload_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from API import views

router = routers.DefaultRouter()
router.register(r'images', views.ImageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('<str:image_name>', views.image_view),
    path('add/', views.add_new_image_view),
    path('tmp/<str:token>', views.temporary_link_view),
    path('tmp-gen/<str:image_name>/<int:seconds>/', views.temporary_link_generator),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
