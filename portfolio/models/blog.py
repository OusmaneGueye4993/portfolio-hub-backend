from django.db import models

class Publication(models.Model):
    TYPE_CHOICES = (
        ('ARTICLE', 'Article'),
        ('CONFERENCE', 'Conférence'),
        ('PRESENTATION', 'Présentation'),
    )
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='ARTICLE')
    content = models.TextField()
    external_link = models.URLField(blank=True, null=True)
    published_date = models.DateField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return f"[{self.get_type_display()}] {self.title}"

class GalleryItem(models.Model):
    title = models.CharField(max_length=255)
    event_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/')
    date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.event_name})"

class Testimonial(models.Model):
    author_name = models.CharField(max_length=150)
    position = models.CharField(max_length=255, help_text="Ex: Enseignant chercheur, Maître de stage")
    company_or_institution = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Recommandation de {self.author_name}"