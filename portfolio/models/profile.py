from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=255, default="Élève Ingénieur en Informatique, Réseaux et Télécommunications")
    bio = models.TextField()
    avatar = models.ImageField(upload_to='profile/')
    cv_file = models.FileField(upload_to='cv/')
    
    # Réseaux Sociaux (Stockés proprement en JSON)
    social_links = models.JSONField(default=dict, help_text="Ex: {'linkedin': 'url', 'github': 'url'}")
    
    # Feature Flags (Activation/Désactivation dynamique des sections)
    is_blog_enabled = models.BooleanField(default=True)
    is_gallery_enabled = models.BooleanField(default=True)
    is_testimonials_enabled = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Portfolio Configuration"

class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name

class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(help_text="Niveau de maîtrise de 0 à 100")

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.name} ({self.category.name}) - {self.level}%"

class Experience(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Laisser vide si poste actuel")
    description = models.TextField()
    skills_used = models.ManyToManyField(Skill, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} chez {self.company}"

class Education(models.Model):
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_year']

    def __str__(self):
        return f"{self.degree} - {self.institution}"