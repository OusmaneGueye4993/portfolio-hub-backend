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
        # On extrait juste le nom du fichier sans les préfixes de dossiers éventuels (ex: 'cv/mon_cv.pdf' -> 'mon_cv.pdf')
        filename = os.path.basename(name)
        base_name, ext = os.path.splitext(filename)
        ext = ext.lower()

        if ext in ['.pdf', '.doc', '.docx', '.zip']:
            # On force le type 'upload' pour garantir l'accès public sans restriction de signature
            result = cloudinary.uploader.upload(
                content,
                public_id=base_name,
                resource_type='image',
                type='upload'
            )
            return result['secure_url']
        else:
            result = cloudinary.uploader.upload(
                content,
                public_id=base_name,
                resource_type='image',
                type='upload'
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
        name = os.path.splitext(os.path.basename(name))[0]
        cloudinary.uploader.destroy(name, resource_type='image')
