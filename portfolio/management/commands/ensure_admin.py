import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or update the production admin account when explicitly enabled."

    def handle(self, *args, **options):
        if os.environ.get("ENSURE_ADMIN", "").lower() != "true":
            self.stdout.write(
                self.style.WARNING(
                    "ENSURE_ADMIN is not true. No admin changes were made."
                )
            )
            return

        username = os.environ.get("ADMIN_USERNAME", "").strip()
        email = os.environ.get("ADMIN_EMAIL", "").strip()
        password = os.environ.get("ADMIN_PASSWORD", "")

        if not username:
            raise CommandError("ADMIN_USERNAME is required.")

        if not email:
            raise CommandError("ADMIN_EMAIL is required.")

        if not password:
            raise CommandError("ADMIN_PASSWORD is required.")

        if len(password) < 12:
            raise CommandError("ADMIN_PASSWORD must be at least 12 characters.")

        User = get_user_model()

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )

        user.email = email
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin account '{username}' is ready."
            )
        )
