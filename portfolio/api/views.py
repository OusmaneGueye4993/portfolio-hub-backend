from rest_framework import viewsets, permissions
from django.core.mail import send_mail
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend

from ..models import (
    UserProfile, SkillCategory, Experience, Education,
    Project, Certification, Publication, GalleryItem, Testimonial, ContactMessage
)
from .serializers import (
    UserProfileSerializer, SkillCategorySerializer, ExperienceSerializer,
    EducationSerializer, ProjectSerializer, CertificationSerializer,
    PublicationSerializer, GalleryItemSerializer, TestimonialSerializer, ContactMessageSerializer
)

class DynamicPermissionMixin:
    """
    Sécurité : Tout le monde peut lire (GET). 
    Seul l'administrateur authentifié par JWT peut modifier (POST, PUT, DELETE).
    """
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class UserProfileViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    # CORRECTION : Utiliser l'attribut standard de Django REST Framework
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        # On retourne uniquement la configuration principale
        return UserProfile.objects.all()[:1]

class SkillCategoryViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
    queryset = SkillCategory.objects.prefetch_related('skills').all()
    serializer_class = SkillCategorySerializer

class ExperienceViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class EducationViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

class ProjectViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related('gallery').all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_featured']

class CertificationViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer

class PublicationViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

class GalleryItemViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

    def get_permissions(self):
        if self.action == 'create': # Un utilisateur anonyme peut proposer un témoignage
            return [permissions.AllowAny()]
        if self.action in ['list', 'retrieve']: # Tout le monde peut lire
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()] # Seul l'admin valide ou supprime

    def get_queryset(self):
        if self.request.user.is_staff:
            return Testimonial.objects.all()
        return Testimonial.objects.filter(is_approved=True)


# class ContactMessageViewSet(viewsets.ModelViewSet):
#     queryset = ContactMessage.objects.all()
#     serializer_class = ContactMessageSerializer

#     def get_permissions(self):
#         if self.action == 'create': # Soumission publique du formulaire
#             return [permissions.AllowAny()]
#         return [permissions.IsAdminUser()] # Consultation réservée à l'admin

#     def perform_create(self, serializer):
#         # 1. On sauvegarde d'abord le message en base de données (Validation immédiate)
#         instance = serializer.save()
        
#         # 2. On tente l'envoi de l'email de manière asynchrone / silencieuse
#         # Si Render bloque le port, l'utilisateur recevra quand même sa confirmation de succès !
#         send_mail(
#             subject=f"[Portfolio] Message de {instance.name} : {instance.subject}",
#             message=f"Nouveau message reçu depuis le Portfolio.\n\n"
#                     f"De : {instance.name} ({instance.email})\n"
#                     f"Sujet : {instance.subject}\n\n"
#                     f"Message :\n{instance.message}",
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[settings.ADMIN_EMAIL],
#             fail_silently=True,  # 🎯 CLÉ DE LA SOLUTION : Évite les Timeouts et renvoie un succès (201 Created)
#         )



class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.action == 'create': # Soumission publique du formulaire
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()] # Consultation réservée à l'admin

    def perform_create(self, serializer):
        # 🎯 LA CORRECTION ICI : On enregistre uniquement en base de données.
        # Cela prend moins de 100 millisecondes et renvoie un succès instantané à React !
        serializer.save()