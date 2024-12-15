# In api/urls.py  

from django.urls import path, include  
from rest_framework.routers import DefaultRouter  
from .views import YourModelViewSet, upload_images  # Import the upload function  

# Initialize the Django REST framework router  
router = DefaultRouter()  
router.register(r'yourmodel', YourModelViewSet)  # Use the same name for your model  

urlpatterns = [  
    path('', include(router.urls)),  
    path('upload/', upload_images, name='upload'),  # Directly call the upload_images function  
]