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
            # Changement : resource_type='image' pour contourner les restrictions strictes du mode raw
            result = cloudinary.uploader.upload(
                content,
                public_id=os.path.splitext(name)[0],
                resource_type='image'
            )
            return result['secure_url']
        else:
            result = cloudinary.uploader.upload(
                content,
                public_id=os.path.splitext(name)[0],
                resource_type='image'
            )
            return result['secure_url']

    def url(self, name):
        if name.startswith('http://') or name.startswith('https://'):
            return name
        return CloudinaryImage(name).build_url()

    def exists(self, name):
        return False

    def delete(self, name):
        if name.startswith('http://') or name.startswith('https://'):
            name = name.split('/upload/')[-1]
            if name.split('/')[0].startswith('v') and name.split('/')[0][1:].isdigit():
                name = '/'.join(name.split('/')[1:])
        name = os.path.splitext(name)[0]
        cloudinary.uploader.destroy(name, resource_type='image')
