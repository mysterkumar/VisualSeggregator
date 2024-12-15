from ninja import Router, File
from ninja.files import UploadedFile
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
from typing import List
# In api/views.py  

from rest_framework import viewsets  
from .models import YourModel  # Make sure your model is imported  
from .serializers import YourModelSerializer  # Make sure your serializer is imported  

class YourModelViewSet(viewsets.ModelViewSet):  
    queryset = YourModel.objects.all()  # Adjust based on your model  
    serializer_class = YourModelSerializer  # Use the serializer you have created
    
api_router = Router()

def extract_image_features(image_path):
    """Extract simple features from an image (e.g., average RGB values)."""
    with Image.open(image_path) as img:
        img = img.resize((100, 100))  # Resize to reduce complexity
        img_array = np.array(img)
        avg_color = img_array.mean(axis=(0, 1))  # Average color
        return avg_color  # Returns [R, G, B]

@api_router.post("/upload/")
def upload_images(
    request,
    images: List[UploadedFile] = File(...),
    similarity_threshold: float = 0.7,
    product_category: str = "Default",
    style: str = "Casual",
    grouping_option: str = "Category",
):
    # Validate the images
    if len(images) > 5:
        return {"error": "You can upload a maximum of 5 images."}

    # Save uploaded images temporarily and extract features
    image_paths = []
    features = []
    for img in images:
        file_path = f"media/{img.name}"
        with open(file_path, 'wb') as f:
            for chunk in img.chunks():
                f.write(chunk)
        image_paths.append(file_path)
        features.append(extract_image_features(file_path))

    # Perform clustering
    n_clusters = min(len(features), 3)  # Example: Max 3 clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(features)

    # Organize output
    clustered_data = {}
    for idx, cluster in enumerate(clusters):
        clustered_data.setdefault(cluster, []).append(image_paths[idx])

    # Example response
    return {
        "message": "Images processed and clustered successfully.",
        "clusters": clustered_data,
        "similarity_threshold": similarity_threshold,
        "product_category": product_category,
        "style": style,
        "grouping_option": grouping_option,
    }
