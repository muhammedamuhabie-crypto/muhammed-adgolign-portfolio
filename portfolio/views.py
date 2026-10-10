from django.http import FileResponse, HttpResponse, HttpResponseRedirect
import logging

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.core.validators import validate_email
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render

from .models import Certification, Certificate, Project, Profile, Contact


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: https://muhammed-adgolign-portfolio.onrender.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


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



@require_POST
def send_contact_message(request):
    name = request.POST.get("name", "").strip()
    sender_email = request.POST.get("email", "").strip()
    subject = request.POST.get("subject", "").strip()
    body = request.POST.get("message", "").strip()

    if not name or not sender_email or not subject or not body:
        messages.error(request, "Please complete all required fields.")
        return HttpResponseRedirect("/#contact")

    if (
        len(name) > 100
        or len(sender_email) > 254
        or len(subject) > 150
        or len(body) > 5000
        or "\r" in subject
        or "\n" in subject
    ):
        messages.error(request, "Please check your entries and try again.")
        return HttpResponseRedirect("/#contact")

    try:
        validate_email(sender_email)
    except ValidationError:
        messages.error(request, "Please enter a valid email address.")
        return HttpResponseRedirect("/#contact")

    contact = Contact.objects.filter(active=True).first()

    if not contact or not contact.email:
        messages.error(
            request,
            "Contact email is not configured yet. Please try again later.",
        )
        return HttpResponseRedirect("/#contact")

    try:
        mailer = settings.MAILERS.get("default", {})
        options = mailer.get("OPTIONS", {})

        if not all(options.get(key) for key in ("host", "username", "password")):
            raise RuntimeError("SMTP settings are incomplete.")

        connection = EmailBackend(
            host=options["host"],
            port=options.get("port", 587),
            username=options["username"],
            password=options["password"],
            use_tls=options.get("use_tls", True),
            use_ssl=False,
            timeout=options.get("timeout", 10),
            ssl_keyfile="",
            ssl_certfile="",
            fail_silently=False,
        )

        email = EmailMessage(
            subject=f"[Portfolio Contact] {subject}",
            body=f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{body}",
            from_email=options["username"],
            to=[contact.email],
            reply_to=[sender_email],
            connection=connection,
        )
        sent_count = email.send(fail_silently=False)

        if sent_count != 1:
            raise RuntimeError("The email service did not accept the message.")

        messages.success(
            request,
            "Your message was sent successfully. Thank you for reaching out!",
        )

    except Exception:
        logging.getLogger(__name__).exception(
            "Portfolio contact message could not be sent."
        )
        messages.error(
            request,
            "Sorry, your message could not be sent right now. Please try again later.",
        )

    return HttpResponseRedirect("/#contact")

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




