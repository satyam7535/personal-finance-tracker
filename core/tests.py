"""
Tests for core app — UserProfile model and authentication views.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.urls import reverse

from allauth.socialaccount.models import SocialApp

from core.models import UserProfile


class UserProfileModelTest(TestCase):
    """Tests for UserProfile auto-creation and preferences."""

    def test_profile_auto_created_on_user_creation(self):
        """UserProfile is auto-created via post_save signal."""
        user = User.objects.create_user('testuser', 'test@example.com', 'pass1234')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, UserProfile)

    def test_default_preferred_currency(self):
        """Default preferred currency is USD."""
        user = User.objects.create_user('testuser', 'test@example.com', 'pass1234')
        self.assertEqual(user.profile.preferred_currency, 'USD')

    def test_profile_str_representation(self):
        user = User.objects.create_user('testuser', 'test@example.com', 'pass1234')
        self.assertEqual(str(user.profile), "testuser's profile")

    def test_profile_update_preferred_currency(self):
        user = User.objects.create_user('testuser', 'test@example.com', 'pass1234')
        user.profile.preferred_currency = 'INR'
        user.profile.save()
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.preferred_currency, 'INR')


class AuthViewsTest(TestCase):
    """Tests for registration, login, logout views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass1234')
        # Create a SocialApp so the login template's {% provider_login_url "google" %} tag works
        site = Site.objects.get_current()
        app = SocialApp.objects.create(
            provider='google', name='Google',
            client_id='test-client-id', secret='test-secret')
        app.sites.add(site)

    def test_register_page_loads(self):
        response = self.client.get(reverse('core:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_register_creates_user(self):
        response = self.client.post(reverse('core:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_page_loads(self):
        response = self.client.get(reverse('core:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_valid_credentials(self):
        response = self.client.post(reverse('core:login'), {
            'username': 'testuser',
            'password': 'pass1234',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('core:login'), {
            'username': 'testuser',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('core:logout'))
        self.assertEqual(response.status_code, 302)

    def test_profile_requires_login(self):
        response = self.client.get(reverse('core:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_loads_for_authenticated_user(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('core:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
