from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class RegistrationAndLoginTests(TestCase):
    def test_user_can_register_with_email_username_and_password(self):
        response = self.client.post(reverse('register'), {
            'username': 'jamie',
            'email': 'jamie@example.com',
            'password1': 'SafePassword123!xyz',
            'password2': 'SafePassword123!xyz',
        })

        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='jamie', email='jamie@example.com').exists())
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_user_can_log_in_with_username_or_email(self):
        user = User.objects.create_user(
            username='jamie',
            email='jamie@example.com',
            password='SafePassword123!xyz',
        )

        for identifier in ('jamie', 'jamie@example.com'):
            with self.subTest(identifier=identifier):
                response = self.client.post(reverse('login'), {
                    'username': identifier,
                    'password': 'SafePassword123!xyz',
                })
                self.assertRedirects(response, reverse('home'))
                self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
                self.client.logout()

    def test_logout_requires_post_and_ends_session(self):
        user = User.objects.create_user(username='jamie', password='SafePassword123!xyz')
        self.client.force_login(user)

        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_registration_rejects_duplicate_email_case_insensitively(self):
        User.objects.create_user(
            username='existing',
            email='used@example.com',
            password='SafePassword123!xyz',
        )
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'USED@example.com',
            'password1': 'AnotherSafePassword123!',
            'password2': 'AnotherSafePassword123!',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already exists')
