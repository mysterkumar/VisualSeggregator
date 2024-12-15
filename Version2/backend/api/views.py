from rest_framework import viewsets
from .models import YourModel
from .serializers import YourModelSerializer
from ninja import Router, File
from ninja.files import UploadedFile
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
from typing import List
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# YourModel ViewSet for CRUD operations
class YourModelViewSet(viewsets.ModelViewSet):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer

# API router for file uploads and processing
api_router = Router()

def extract_image_features(image_path):
    """Extract simple features from an image (e.g., average RGB values)."""
    try:
        with Image.open(image_path) as img:
            img = img.resize((100, 100))
            img_array = np.array(img)
            avg_color = img_array.mean(axis=(0, 1))  # Average color
            return avg_color.tolist()
    except Exception as e:
        raise ValueError(f"Failed to process image: {e}")

@csrf_exempt
@api_router.post("/upload/")
def upload_images(
    request,
    similarity_threshold: float = 0.7,
    product_category: str = "Default",
    style: str = "Casual",
    grouping_option: str = "Category",
):
    try:
        images = request.FILES.getlist("images")
        if len(images) > 5:
            return JsonResponse({"error": "You can upload a maximum of 5 images."}, status=400)

        image_paths = []
        features = []
        for img in images:
            file_path = f"media/{img.name}"
            with open(file_path, 'wb') as f:
                for chunk in img.chunks():
                    f.write(chunk)
            image_paths.append(file_path)
            features.append(extract_image_features(file_path))

        n_clusters = min(len(features), 3)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(features)

        clustered_data = {}
        for idx, cluster in enumerate(clusters):
            clustered_data.setdefault(cluster, []).append(image_paths[idx])

        return JsonResponse({
            "message": "Images processed and clustered successfully.",
            "clusters": clustered_data,
            "similarity_threshold": similarity_threshold,
            "product_category": product_category,
            "style": style,
            "grouping_option": grouping_option,
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
