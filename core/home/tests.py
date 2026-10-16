from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import MemberStatus, WorkspaceInvite, car


User = get_user_model()


class AuthenticatedDashboardTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='jamie',
			email='jamie@example.com',
			password='ValidPassword123!',
		)
		self.client.force_login(self.user)

	def test_dashboard_requires_authentication(self):
		self.client.logout()
		response = self.client.get(reverse('home'))

		self.assertRedirects(response, f"{reverse('login')}?next=/")

	def test_invited_person_appears_and_can_be_deleted(self):
		response = self.client.post(reverse('invite'), {
			'name': 'Taylor Reed',
			'email': 'taylor@example.com',
			'role': 'Researcher',
			'team': 'Design',
		}, follow=True)

		invite = WorkspaceInvite.objects.get(owner=self.user, email='taylor@example.com')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Taylor Reed')
		self.assertContains(response, 'taylor@example.com')
		self.assertContains(response, 'Invited')

		response = self.client.post(reverse('delete_invite', args=[invite.pk]), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertFalse(WorkspaceInvite.objects.filter(pk=invite.pk).exists())
		self.assertNotContains(response, 'taylor@example.com')

	def test_duplicate_email_is_rejected(self):
		User.objects.create_user(
			username='registered',
			email='john.carter@example.com',
			password='ValidPassword123!',
		)
		response = self.client.post(reverse('invite'), {
			'name': 'Existing Person',
			'email': 'john.carter@example.com',
		})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'already in the directory')

	def test_registered_users_are_listed_and_can_toggle_own_availability(self):
		status = MemberStatus.objects.get(user=self.user)
		self.assertTrue(status.is_available)

		response = self.client.get(reverse('home'))
		self.assertContains(response, 'Registered user')
		self.assertContains(response, 'Make inactive')
		self.assertContains(response, 'John Carter')
		self.assertContains(response, 'Jane Cooper')

		response = self.client.get(reverse('overview'))
		self.assertContains(response, 'jamie')
		self.assertContains(response, 'Make inactive')

		response = self.client.post(reverse('toggle_member_status'))
		self.assertRedirects(response, reverse('home'))
		status.refresh_from_db()
		self.assertFalse(status.is_available)
		self.user.refresh_from_db()
		self.assertTrue(self.user.is_active)

		for page in ('home', 'overview'):
			with self.subTest(page=page):
				response = self.client.get(reverse(page))
				self.assertContains(response, 'Inactive')
				self.assertContains(response, 'Make active')

		other_user = User.objects.create_user(
			username='other',
			email='other@example.com',
			password='ValidPassword123!',
		)
		self.client.force_login(other_user)
		self.client.post(reverse('toggle_member_status'))

		status.refresh_from_db()
		self.assertFalse(status.is_available)
		self.assertFalse(MemberStatus.objects.get(user=other_user).is_available)

	def test_cars_are_private_to_their_owner_and_render_on_both_pages(self):
		car.objects.create(car_name='Toyota', owner=self.user)

		other_user = User.objects.create_user(
			username='other',
			email='other@example.com',
			password='ValidPassword123!',
		)
		for page in ('home', 'overview'):
			with self.subTest(page=page):
				response = self.client.get(reverse(page))
				self.assertEqual(response.status_code, 200)
				self.assertContains(response, 'Toyota')
				self.assertContains(response, 'Active')

		self.client.force_login(other_user)
		response = self.client.get(reverse('home'))
		self.assertEqual(len(response.context['cars']), 0)

	def test_user_can_add_and_toggle_car_active_state(self):
		response = self.client.post(reverse('add_car'), {'car_name': 'Maruti Suzuki'})
		self.assertRedirects(response, reverse('home'))
		owned_car = car.objects.get(owner=self.user, car_name='Maruti Suzuki')
		self.assertTrue(owned_car.is_active)

		response = self.client.post(reverse('toggle_car', args=[owned_car.pk]))
		self.assertRedirects(response, reverse('home'))
		owned_car.refresh_from_db()
		self.assertFalse(owned_car.is_active)

	def test_legacy_unowned_cars_remain_visible(self):
		car.objects.create(car_name='Toyota')

		response = self.client.get(reverse('home'))

		self.assertContains(response, 'Toyota')
		self.assertContains(response, 'Shared')

	def test_user_cannot_delete_another_users_invite_or_toggle_their_car(self):
		other_user = User.objects.create_user(
			username='other',
			email='other@example.com',
			password='ValidPassword123!',
		)
		invite = WorkspaceInvite.objects.create(
			owner=other_user,
			name='Another user',
			email='another@example.com',
		)
		other_car = car.objects.create(car_name='Hyundai', owner=other_user)

		self.assertEqual(
			self.client.post(reverse('delete_invite', args=[invite.pk])).status_code,
			404,
		)
		self.assertEqual(
			self.client.post(reverse('toggle_car', args=[other_car.pk])).status_code,
			404,
		)
