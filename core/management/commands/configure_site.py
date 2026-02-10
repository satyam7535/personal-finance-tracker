"""
Management command to configure the Django Site object for the current domain.
This is essential for django-allauth social authentication to work properly.
"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Configure the Django Site domain from BASE_URL setting'

    def handle(self, *args, **options):
        # Extract domain from BASE_URL
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
