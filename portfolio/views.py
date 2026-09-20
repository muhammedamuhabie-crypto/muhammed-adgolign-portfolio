from django.http import FileResponse
from django.shortcuts import get_object_or_404, render

from .models import Certification, Certificate, Project, Profile, Contact


def home(request):
    certifications = Certification.objects.prefetch_related("certificates")
    projects = Project.objects.filter(published=True).order_by("order", "id")
    profile = Profile.objects.first()
    contact = Contact.objects.filter(active=True).first()

    return render(
        request,
        "portfolio/home.html",
        {
            "certifications": certifications,
            "projects": projects,
            "profile": profile,
            "contact": contact,
        },
    )


def certificate_view(request, certificate_id):
    certificate = get_object_or_404(
        Certificate.objects.select_related("certification"),
        id=certificate_id,
    )

    return render(
        request,
        "portfolio/certificate_view.html",
        {
            "certificate": certificate,
        },
    )


def certificate_file_view(request, certificate_id):
    certificate = get_object_or_404(
        Certificate.objects.select_related("certification"),
        id=certificate_id,
    )

    response = FileResponse(
        certificate.file.open("rb"),
        content_type="application/pdf",
    )
    response["Content-Disposition"] = "inline"
    response["X-Frame-Options"] = "SAMEORIGIN"

    return response

def certification_view(request, certification_id):
    certification = get_object_or_404(
        Certification.objects.prefetch_related("certificates"),
        id=certification_id,
    )

    return render(
        request,
        "portfolio/certification_view.html",
        {
            "certification": certification,
        },
    )
