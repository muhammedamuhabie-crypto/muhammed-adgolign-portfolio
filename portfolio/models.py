from django.db import models


class Certification(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name


class Certificate(models.Model):
    certification = models.ForeignKey(
        Certification,
        on_delete=models.CASCADE,
        related_name="certificates"
    )
    title = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to="certificates/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        if self.title:
            return f"{self.certification.name} - {self.title}"
        return self.certification.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    category = models.CharField(max_length=150, blank=True)
    description = models.TextField()
    technologies = models.CharField(max_length=500, blank=True)
    visual_type = models.CharField(max_length=30, default="standard")
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    research_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title
class Profile(models.Model):
    name = models.CharField(max_length=200, default="MUHAMMED ADGOLIGN")
    role = models.CharField(
        max_length=300,
        default="Nuclear Engineering Student - Software Developer - Researcher"
    )
    description = models.TextField(
        blank=True,
        default="Nuclear Engineering student, software developer, and researcher passionate about software development, engineering research, and building practical technical projects."
    )
    image = models.ImageField(upload_to="profile/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Contact(models.Model):
    email = models.EmailField(blank=True)
    whatsapp_url = models.URLField(blank=True)
    telegram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email or "Contact Information"