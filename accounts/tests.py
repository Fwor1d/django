from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from .models import Profile

User = get_user_model()


class AccountTests(TestCase):
    def test_signup_and_profile_autocreation(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser", "email": "new@example.com",
            "password1": "BetterTestPassword123!", "password2": "BetterTestPassword123!",
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="newuser")
        self.assertEqual(user.email, "new@example.com")
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertEqual(self.client.get(reverse("profile")).status_code, 200)

    def test_update_profile(self):
        user = User.objects.create_user(username="owner", password="BetterTestPassword123!", email="owner@example.com")
        self.client.force_login(user)
        response = self.client.post(reverse("profile_edit"), {
            "first_name": "Георгий", "last_name": "Тест", "email": "owner@example.com",
            "bio": "О себе", "location": "Москва", "birth_date": "2003-01-01",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Profile.objects.get(user=user).location, "Москва")

    def test_password_reset_console(self):
        User.objects.create_user(username="mailuser", password="BetterTestPassword123!", email="mail@example.com")
        response = self.client.post(reverse("password_reset"), {"email": "mail@example.com"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("/accounts/reset/", mail.outbox[0].body)

    def test_login_page(self):
        self.assertEqual(self.client.get(reverse("login")).status_code, 200)
        self.assertEqual(self.client.get(reverse("password_reset")).status_code, 200)
