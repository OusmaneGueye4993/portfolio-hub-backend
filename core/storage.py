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

        # Si c'est un document, on l'envoie en tant que 'raw'
        if ext in ['.pdf', '.doc', '.docx', '.zip']:
            result = cloudinary.uploader.upload(
                content,
                public_id=base_name,
                resource_type='raw'
            )
            return result['secure_url']
        else:
            result = cloudinary.uploader.upload(
                content,
                public_id=base_name,
                resource_type='image'
            )
            return result['secure_url']

    def url(self, name):
        # 1. Si 'name' est déjà une URL complète (ce que Django stocke souvent)
        if name.startswith('http://') or name.startswith('https://'):
            # CORRECTION CRUCIALE : Si c'est un PDF et qu'il a été taggué /image/, on corrige l'URL à la volée
            if '.pdf' in name.lower() and '/image/upload/' in name:
                return name.replace('/image/upload/', '/raw/upload/')
            return name
        
        # 2. Si Django n'a stocké que le nom du fichier / public_id
        ext = os.path.splitext(name)[1].lower()
        r_type = 'raw' if ext in ['.pdf', '.doc', '.docx', '.zip'] else 'image'
        
        try:
            # On demande au SDK de générer l'URL propre avec le bon type de ressource
            url, _ = cloudinary_url(name, resource_type=r_type, secure=True)
            return url
        except Exception:
            return name

    def exists(self, name):
        return False

    def delete(self, name):
        if name.startswith('http://') or name.startswith('https://'):
            r_type = 'raw' if '.pdf' in name or '.zip' in name else 'image'
            name = name.split('/upload/')[-1]
            if name.split('/')[0].startswith('v') and name.split('/')[0][1:].isdigit():
                name = '/'.join(name.split('/')[1:])
        else:
            ext = os.path.splitext(name)[1].lower()
            r_type = 'raw' if ext in ['.pdf', '.doc', '.docx', '.zip'] else 'image'
            
        name = os.path.splitext(os.path.basename(name))[0]
        try:
            cloudinary.uploader.destroy(name, resource_type=r_type)
        except Exception:
            pass
