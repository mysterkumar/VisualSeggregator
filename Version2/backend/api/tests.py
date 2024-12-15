from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import YourModel

class YourModelTests(TestCase):
    def test_model_creation(self):
        obj = YourModel.objects.create(name="Test Model", description="This is a test.")
        self.assertEqual(obj.name, "Test Model")
        self.assertEqual(obj.description, "This is a test.")

    def test_upload_images_endpoint(self):
        image = SimpleUploadedFile("test.jpg", b"image_content", content_type="image/jpeg")
        response = self.client.post("/api/upload/", {"images": [image]})
        self.assertEqual(response.status_code, 200)
