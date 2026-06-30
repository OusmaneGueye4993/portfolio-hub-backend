from rest_framework import serializers
from ..models import (
    UserProfile, SkillCategory, Skill, Experience, Education,
    ProjectCategory, Project, ProjectGallery, Certification,
    Publication, GalleryItem, Testimonial, ContactMessage
)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class SkillCategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'order', 'skills']
        extra_kwargs = {
            'order': {'required': False, 'default': 1}
        }

class ExperienceSerializer(serializers.ModelSerializer):
    skills_used_detail = SkillSerializer(many=True, source='skills_used', read_only=True)

    class Meta:
        model = Experience
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class ProjectGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectGallery
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    gallery = ProjectGallerySerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'

class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'



# À AJOUTER dans serializers.py pour permettre le CRUD des tables de jointures/catégories :

class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = '__all__'

# Note : Ton SkillCategorySerializer actuel embarque les skills en read_only.
# Pour créer/modifier une catégorie seule sans contrainte, ce serializer standard est idéal :
class SkillCategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = '__all__'