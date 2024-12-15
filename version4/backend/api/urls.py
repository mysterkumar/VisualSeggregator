from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import upload_images, UploadedImageViewSet

router = DefaultRouter()
router.register(r'uploadedimages', UploadedImageViewSet, basename='uploadedimage')

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', upload_images, name='upload'),
]
