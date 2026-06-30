from django.contrib import admin
from ..models import (
    UserProfile, SkillCategory, Skill, Experience, Education,
    ProjectCategory, Project, ProjectGallery, Certification,
    Publication, GalleryItem, Testimonial, ContactMessage
)

# Inline pour inclure la galerie directement sur la page du projet associé
class ProjectGalleryInline(admin.TabularInline):
    model = ProjectGallery
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'order')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'technologies')
    inlines = [ProjectGalleryInline]

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'received_at', 'is_read')
    list_filter = ('is_read', 'received_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'received_at')

# Enregistrement simple pour le reste
admin.site.register(UserProfile)
admin.site.register(SkillCategory)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(ProjectCategory)
admin.site.register(Certification)
admin.site.register(Publication)
admin.site.register(GalleryItem)
admin.site.register(Testimonial)