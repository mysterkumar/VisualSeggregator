from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.conf import settings  # Import settings for relative paths
from .models import UploadedImage
from .serializers import UploadedImageSerializer
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
import os  # To handle relative paths

def extract_image_features(image_path):
    """Extract features from an image."""
    try:
        print(f"Processing image at: {image_path}")  # Log the image path
        with Image.open(image_path) as img:
            img = img.convert("RGB")  # Ensure the image is RGB
            img = img.resize((100, 100))  # Resize to 100x100 pixels
            img_array = np.array(img)
            avg_color = img_array.mean(axis=(0, 1))  # Compute average [R, G, B]
            print(f"Extracted features: {avg_color}")  # Log the extracted features
            return avg_color.tolist()
    except Exception as e:
        print(f"Error processing image at {image_path}: {e}")  # Log any error
        return None

@api_view(['POST'])
def upload_images(request):
    """
    Handle image uploads, feature extraction, and clustering.
    """
    print("Received request for image upload")
    print("Request method:", request.method)
    print("Request content type:", request.content_type)
    print("Files received:", request.FILES)
    images = request.FILES.getlist('images')
    print(f"Number of images received: {len(images)}")
    
    if len(images) == 0:
        return Response({"error": "No images were submitted."}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(images) > 5:
        return Response({"error": "You can upload a maximum of 5 images."}, status=status.HTTP_400_BAD_REQUEST)

    image_paths = []
    features = []

    for img in images:
        try:
            # Save the image
            uploaded_image = UploadedImage(image=img)
            uploaded_image.save()
            file_path = uploaded_image.image.path
            print(f"Image saved at: {file_path}")

            # Extract features
            feature = extract_image_features(file_path)
            if feature is not None:
                image_paths.append(file_path)
                features.append(feature)
            else:
                print(f"Skipping invalid image: {file_path}")
        except Exception as e:
            print(f"Error while processing image: {e}")
            return Response({"error": f"Failed to process image {img.name}: {e}"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate the features
    if not features:
        return Response({"error": "Failed to process images. Ensure all uploaded images are valid."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Perform clustering
    n_clusters = min(len(features), 3)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(features)

    # Organize output with relative paths
    clustered_data = {i: [] for i in range(n_clusters)}
    for idx, cluster in enumerate(clusters):
        # Get relative path and append it
        relative_path = os.path.relpath(image_paths[idx], settings.MEDIA_ROOT)
        clustered_data[cluster].append(f"media/{relative_path}")

    return Response({
        "message": "Images processed and clustered successfully.",
        "clusters": clustered_data,
    })

# Add this ViewSet for image management
class UploadedImageViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing uploaded images.
    """
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer
