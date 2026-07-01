import os
import cloudinary
import cloudinary.uploader
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

        # Détermination du type de ressource Cloudinary
        if ext in ['.pdf', '.doc', '.docx', '.zip']:
            r_type = 'raw'
        else:
            r_type = 'image'

        # Upload avec le bon type et définition explicite de l'accès public
        result = cloudinary.uploader.upload(
            content,
            public_id=base_name,
            resource_type=r_type,
            type='upload'  # Force l'accès public sans restriction de signature
        )
        
        # On retourne l'URL sécurisée complète générée directement par la réponse Cloudinary
        return result['secure_url']

    def url(self, name):
        # Si le nom est déjà une URL complète, on la retourne
        if name.startswith('http://') or name.startswith('https://'):
            return name
        
        # Fallback de sécurité si seul le public_id ou un chemin relatif est stocké
        ext = os.path.splitext(name)[1].lower()
        r_type = 'raw' if ext in ['.pdf', '.doc', '.docx', '.zip'] else 'image'
        
        try:
            return cloudinary.CloudinaryResource(name, resource_type=r_type).build_url(secure=True)
        except Exception:
            return name

    def exists(self, name):
        return False

    def delete(self, name):
        if name.startswith('http://') or name.startswith('https://'):
            # Extraction du type et du public_id depuis l'URL
            r_type = 'raw' if '.pdf' in name or '.zip' in name else 'image'
            name = name.split('/upload/')[-1]
            if name.split('/')[0].startswith('v') and name.split('/')[0][1:].isdigit():
                name = '/'.join(name.split('/')[1:])
            cloudinary.uploader.destroy(name, resource_type=r_type)
