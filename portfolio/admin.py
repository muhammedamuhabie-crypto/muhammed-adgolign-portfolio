from django.contrib import admin

from .models import Certification, Certificate, Project, Profile, Contact


class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 1
    fields = ("title", "file", "order")


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("name", "certificate_count", "created_at")
    search_fields = ("name",)
    inlines = [CertificateInline]

    def certificate_count(self, obj):
        return obj.certificates.count()

    certificate_count.short_description = "Certificates"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "visual_type", "image_status", "published", "order", "created_at")
    list_filter = ("published", "category")
    search_fields = ("title", "subtitle", "category", "description", "technologies", "visual_type")
    ordering = ("order", "id")
    @admin.display(boolean=True, description="Image")
    def image_status(self, obj):
        return bool(obj.image)

    fieldsets = (
        (
            "Project Information",
            {
                "fields": (
                    "title",
                    "subtitle",
                    "category",
                    "description",
                    "technologies",
                )
            },
        ),
        (
            "Visual",
            {
                "fields": (
                    "visual_type",
                    "image",
                )
            },
        ),
        (
            "Links",
            {
                "fields": (
                    "live_url",
                    "github_url",
                    "research_url",
                )
            },
        ),
        (
            "Display",
            {
                "fields": (
                    "order",
                    "published",
                )
            },
        ),
    )
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "updated_at")
    search_fields = ("name", "role", "description")
    fieldsets = (
        (
            "Profile Information",
            {
                "fields": (
                    "name",
                    "role",
                    "description",
                    "image",
                )
            },
        ),
    )
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "active", "updated_at")
    list_filter = ("active",)
    search_fields = ("email",)
    fieldsets = (
        (
            "Contact Information",
            {
                "fields": (
                    "email",
                    "whatsapp_url",
                    "telegram_url",
                    "linkedin_url",
                    "github_url",
                ),
            },
        ),
        (
            "Display",
            {
                "fields": ("active",),
            },
        ),
    )