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
            # On uploade en raw
            result = cloudinary.uploader.upload(
                content,
                public_id=name,
                resource_type='raw'
            )
            # ICI LE CHANGEMENT : On retourne l'URL absolue directe (avec sa version et tout)
            # pour qu'elle soit enregistrée directement dans votre base de données.
            return result['secure_url']
        else:
            result = cloudinary.uploader.upload(
                content,
                public_id=os.path.splitext(name)[0],
                resource_type='image'
            )
            return result['public_id']

    def url(self, name):
        # Si le nom commence déjà par http, c'est l'URL absolue qu'on a stockée dans _save
        if name.startswith('http://') or name.startswith('https://'):
            return name
            
        ext = os.path.splitext(name)[1].lower()
        if ext in ['.pdf', '.doc', '.docx', '.zip']:
            cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME']
            return f"https://res.cloudinary.com/{cloud_name}/raw/upload/{name}"
            
        return CloudinaryImage(name).build_url()

    def exists(self, name):
        return False

    def delete(self, name):
        if name.startswith('http://') or name.startswith('https://'):
            # Extrait le public_id de l'URL si on doit supprimer
            name = name.split('/upload/')[-1]
            # Enlever une éventuelle version (ex: v1234567/) du nom
            if name.split('/')[0].startswith('v') and name.split('/')[0][1:].isdigit():
                name = '/'.join(name.split('/')[1:])
                
        ext = os.path.splitext(name)[1].lower()
        res_type = 'raw' if ext in ['.pdf', '.doc', '.docx', '.zip'] else 'image'
        cloudinary.uploader.destroy(name, resource_type=res_type)
