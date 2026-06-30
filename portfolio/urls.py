from django.urls import path, include
from django.conf import settings  # 👈 AJOUTÉ
from django.conf.urls.static import static  # 👈 AJOUTÉ
from rest_framework.routers import DefaultRouter
from .api.views import (
    UserProfileViewSet, SkillCategoryViewSet, ExperienceViewSet,
    EducationViewSet, ProjectViewSet, CertificationViewSet,
    PublicationViewSet, GalleryItemViewSet, TestimonialViewSet, ContactMessageViewSet
)

from .api.views_admin import (
    UserProfileAdminViewSet, SkillCategoryAdminViewSet, SkillAdminViewSet,
    ExperienceAdminViewSet, EducationAdminViewSet, ProjectCategoryAdminViewSet,
    ProjectAdminViewSet, ProjectGalleryAdminViewSet, CertificationAdminViewSet,
    PublicationAdminViewSet, GalleryItemAdminViewSet, TestimonialAdminViewSet,
    ContactMessageAdminViewSet
)

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'skills', SkillCategoryViewSet, basename='skills')
router.register(r'experiences', ExperienceViewSet, basename='experiences')
router.register(r'educations', EducationViewSet, basename='educations')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'certifications', CertificationViewSet, basename='certifications')
router.register(r'publications', PublicationViewSet, basename='publications')
router.register(r'gallery', GalleryItemViewSet, basename='gallery')
router.register(r'testimonials', TestimonialViewSet, basename='testimonials')
router.register(r'contact', ContactMessageViewSet, basename='contact')


# 2. Routeur pour l'administration (CRUD complet sécurisé pour l'Admin)
admin_router = DefaultRouter()
admin_router.register(r'profile', UserProfileAdminViewSet, basename='admin-profile')
admin_router.register(r'skill-categories', SkillCategoryAdminViewSet, basename='admin-skill-category')
admin_router.register(r'skills', SkillAdminViewSet, basename='admin-skill')
admin_router.register(r'experiences', ExperienceAdminViewSet, basename='admin-experience')
admin_router.register(r'educations', EducationAdminViewSet, basename='admin-education')
admin_router.register(r'project-categories', ProjectCategoryAdminViewSet, basename='admin-project-category')
admin_router.register(r'projects', ProjectAdminViewSet, basename='admin-project')
admin_router.register(r'project-galleries', ProjectGalleryAdminViewSet, basename='admin-project-gallery')
admin_router.register(r'certifications', CertificationAdminViewSet, basename='admin-certification')
admin_router.register(r'publications', PublicationAdminViewSet, basename='admin-publication')
admin_router.register(r'gallery-items', GalleryItemAdminViewSet, basename='admin-gallery-item')
admin_router.register(r'testimonials', TestimonialAdminViewSet, basename='admin-testimonial')
admin_router.register(r'messages', ContactMessageAdminViewSet, basename='admin-message')



urlpatterns = [
    path('', include(router.urls)),

    # Routes privées de gestion pour le panneau d'administration React
    path('dashboard-api/', include(admin_router.urls)),
]

# 👇 AJOUTE CETTE CONDITION TOUT EN BAS :
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)