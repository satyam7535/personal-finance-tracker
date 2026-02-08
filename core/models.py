from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extended user profile with financial preferences.
    Auto-created when a User is registered.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferred_currency = models.CharField(
        max_length=3,
        default='USD',
        help_text='ISO 4217 currency code (e.g., USD, EUR, INR)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Auto-create UserProfile when a new User is created."""
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        # Handle case where profile doesn't exist yet (e.g., superuser)
        UserProfile.objects.get_or_create(user=instance)
