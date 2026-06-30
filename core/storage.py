import cloudinary
import cloudinary.uploader
from django.core.files.storage import Storage
from django.conf import settings
import os

class CloudinaryStorage(Storage):
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
        )

    def _save(self, name, content):
        result = cloudinary.uploader.upload(content, public_id=os.path.splitext(name)[0])
        return result['public_id']

    def url(self, name):
        return cloudinary.CloudinaryImage(name).build_url()

    def exists(self, name):
        return False

    def delete(self, name):
        cloudinary.uploader.destroy(name)
