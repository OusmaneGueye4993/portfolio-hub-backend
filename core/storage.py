import os
import cloudinary
import cloudinary.uploader
from cloudinary import CloudinaryImage
from django.core.files.storage import Storage
from django.conf import settings


class CloudinaryStorage(Storage):
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
        )

    def _save(self, name, content):
        ext = os.path.splitext(name)[1].lower()
        if ext in ['.pdf', '.doc', '.docx', '.zip']:
            result = cloudinary.uploader.upload(
                content,
                public_id=os.path.splitext(name)[0],
                resource_type='raw'
            )
            return result['public_id'] + ext
        else:
            result = cloudinary.uploader.upload(
                content,
                public_id=os.path.splitext(name)[0],
                resource_type='image'
            )
            return result['public_id']

    def url(self, name):
        ext = os.path.splitext(name)[1].lower()
        if ext in ['.pdf', '.doc', '.docx', '.zip']:
            cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME']
            return f"https://res.cloudinary.com/{cloud_name}/raw/upload/{name}"
        return CloudinaryImage(name).build_url()

    def exists(self, name):
        return False

    def delete(self, name):
        cloudinary.uploader.destroy(name)
