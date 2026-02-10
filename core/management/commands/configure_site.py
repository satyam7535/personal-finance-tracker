"""
Management command to configure the Django Site object and Google OAuth SocialApp.
This is essential for django-allauth social authentication to work properly.
"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings

from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Configure the Django Site domain and Google OAuth SocialApp from environment settings'

    def handle(self, *args, **options):
        # ── 1. Configure Site domain ────────────────────────────────────────
        base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')

        # Remove protocol
        domain = base_url.replace('https://', '').replace('http://', '')

        # Remove trailing slash if present
        domain = domain.rstrip('/')

        # Remove port if it's localhost
        if ':' in domain and 'localhost' in domain:
            domain = domain.split(':')[0]

        # Get or update the Site object (SITE_ID = 1)
        site_id = getattr(settings, 'SITE_ID', 1)

        site, created = Site.objects.update_or_create(
            id=site_id,
            defaults={
                'domain': domain,
                'name': 'Finance Tracker',
            }
        )

        action = 'Created' if created else 'Updated'
        self.stdout.write(
            self.style.SUCCESS(
                f'{action} Site: domain="{site.domain}", name="{site.name}"'
            )
        )

        # ── 2. Configure Google OAuth SocialApp ─────────────────────────────
        client_id = getattr(settings, 'GOOGLE_CLIENT_ID', '')
        client_secret = getattr(settings, 'GOOGLE_CLIENT_SECRET', '')

        if not client_id or not client_secret:
            self.stdout.write(
                self.style.WARNING(
                    'GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not set — '
                    'skipping Google OAuth SocialApp configuration.'
                )
            )
            return

        social_app, app_created = SocialApp.objects.update_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': client_id,
                'secret': client_secret,
            }
        )

        # Link the SocialApp to the current Site (idempotent)
        if not social_app.sites.filter(id=site.id).exists():
            social_app.sites.add(site)

        app_action = 'Created' if app_created else 'Updated'
        self.stdout.write(
            self.style.SUCCESS(
                f'{app_action} Google SocialApp: client_id="{client_id[:20]}..." '
                f'linked to site "{site.domain}"'
            )
        )
