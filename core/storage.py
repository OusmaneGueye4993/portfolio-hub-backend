import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
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
        filename = os.path.basename(name)
        base_name, ext = os.path.splitext(filename)
        ext = ext.lower()

        if ext in ['.pdf', '.doc', '.docx', '.zip']:
            # On uploade en mode 'image' mais SANS l'extension .pdf dans le public_id
            result = cloudinary.uploader.upload(
                content,
                public_id=base_name,
                resource_type='image'
            )
            
            # On génère l'URL officielle via le SDK en forçant le format PDF
            # Cela produira une URL publique valide et accessible du type .../upload/v12345/CV_Ousmane_Gueye.pdf
            url, _ = cloudinary_url(
                result['public_id'],
                resource_type='image',
                format=ext.replace('.', ''), # force le format pdf
                secure=True
            )
            return url
        else:
            result = cloudinary.uploader.upload(
                content,
                public_id=base_name,
                resource_type='image'
            )
            return result['secure_url']

    def url(self, name):
        if name.startswith('http://') or name.startswith('https://'):
            return name
        return cloudinary_url(name, secure=True)[0]

    def exists(self, name):
        return False

    def delete(self, name):
        if name.startswith('http://') or name.startswith('https://'):
            name = name.split('/upload/')[-1]
            # Supprime la version si présente
            if name.split('/')[0].startswith('v') and name.split('/')[0][1:].isdigit():
                name = '/'.join(name.split('/')[1:])
        # On extrait le public_id pur sans extension
        name = os.path.splitext(os.path.basename(name))[0]
        cloudinary.uploader.destroy(name, resource_type='image')
