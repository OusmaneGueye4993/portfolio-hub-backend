from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from ..models import (
    UserProfile, SkillCategory, Skill, Experience, Education,
    ProjectCategory, Project, ProjectGallery, Certification,
    Publication, GalleryItem, Testimonial, ContactMessage
)
from .serializers import (
    UserProfileSerializer, SkillCategorySerializer, SkillSerializer, ExperienceSerializer,
    EducationSerializer, ProjectCategorySerializer, ProjectSerializer, ProjectGallerySerializer, 
    CertificationSerializer, PublicationSerializer, GalleryItemSerializer, TestimonialSerializer, 
    ContactMessageSerializer
)

# 🔒 Classe de base pour appliquer la sécurité Admin de manière globale
class BaseAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

# --- CRUD CONFIGURATION PROFILE ---
class UserProfileAdminViewSet(BaseAdminViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class SkillCategoryAdminViewSet(BaseAdminViewSet):
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer

class SkillAdminViewSet(BaseAdminViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class ExperienceAdminViewSet(BaseAdminViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class EducationAdminViewSet(BaseAdminViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


# --- CRUD PROJETS ---
class ProjectCategoryAdminViewSet(BaseAdminViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer

class ProjectAdminViewSet(BaseAdminViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectGalleryAdminViewSet(BaseAdminViewSet):
    queryset = ProjectGallery.objects.all()
    serializer_class = ProjectGallerySerializer

class CertificationAdminViewSet(BaseAdminViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer


# --- CRUD BLOG, GALLERIE & RECOMMANDATIONS ---
class PublicationAdminViewSet(BaseAdminViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

class GalleryItemAdminViewSet(BaseAdminViewSet):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer

class TestimonialAdminViewSet(BaseAdminViewSet):
    """
    Ici, l'admin a accès à TOUS les témoignages (approuvés ou non) 
    pour pouvoir les modérer (passer 'is_approved' à True), les modifier ou les supprimer.
    """
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


# --- CRUD MESSAGES DE CONTACT ---
class ContactMessageAdminViewSet(BaseAdminViewSet):
    """
    Permet à l'administrateur de lister les messages reçus, 
    les marquer comme lus ('is_read'=True) ou les supprimer après traitement.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer