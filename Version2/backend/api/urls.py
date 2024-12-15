from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import YourModelViewSet, api_router

# DRF router for YourModel
router = DefaultRouter()
router.register(r'yourmodel', YourModelViewSet)

urlpatterns = [
    path('', include(router.urls)),  # YourModel CRUD endpoints
    path('api/', api_router.urls),  # Ninja API for uploads
]
