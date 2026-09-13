from django.contrib import admin
from django.test import RequestFactory, TestCase

from doctors.models import DoctorProfile, Specialty

from .models import CustomUser


class UserAdminCreationTests(TestCase):
	def setUp(self):
		self.admin_user = CustomUser.objects.create_superuser(
			email='admin-test@example.com',
			password='ValidAdminPassword123!',
		)
		request = RequestFactory().get('/admin/accounts/customuser/add/')
		request.user = self.admin_user
		self.user_admin = admin.site._registry[CustomUser]
		self.user_form_class = self.user_admin.get_form(request)
		self.profile_formset_class = self.user_admin.get_inline_instances(request)[0].get_formset(request)
		self.specialty = Specialty.objects.create(name='Test Specialty')

	def test_admin_can_create_normal_user_without_profile(self):
		form = self.user_form_class({
			'email': 'client-admin-test@example.com',
			'password1': 'ValidClientPassword123!',
			'password2': 'ValidClientPassword123!',
			'role': CustomUser.Role.CLIENT,
			'is_active': 'on',
		})

		self.assertTrue(form.is_valid(), form.errors)
		user = form.save()

		self.assertEqual(user.role, CustomUser.Role.CLIENT)
		self.assertFalse(DoctorProfile.objects.filter(user=user).exists())

	def test_admin_can_create_doctor_with_profile(self):
		form = self.user_form_class({
			'email': 'doctor-admin-test@example.com',
			'password1': 'ValidDoctorPassword123!',
			'password2': 'ValidDoctorPassword123!',
			'role': CustomUser.Role.DOCTOR,
			'is_active': 'on',
		})

		self.assertTrue(form.is_valid(), form.errors)
		user = form.save(commit=False)
		user.save()

		prefix = self.profile_formset_class.get_default_prefix()
		formset = self.profile_formset_class({
			f'{prefix}-TOTAL_FORMS': '1',
			f'{prefix}-INITIAL_FORMS': '0',
			f'{prefix}-MIN_NUM_FORMS': '0',
			f'{prefix}-MAX_NUM_FORMS': '1',
			f'{prefix}-0-specialty': self.specialty.pk,
			f'{prefix}-0-license_number': 'TEST-LICENSE-001',
			f'{prefix}-0-qualifications': 'MD',
			f'{prefix}-0-bio': '',
			f'{prefix}-0-consultation_fee': '75.00',
			f'{prefix}-0-whatsapp_number': '',
			f'{prefix}-0-availability_status': DoctorProfile.AvailabilityStatus.OFFLINE,
			f'{prefix}-0-is_verified': 'on',
		}, instance=user)

		self.assertTrue(formset.is_valid(), formset.errors)
		formset.save()

		profile = DoctorProfile.objects.get(user=user)
		self.assertEqual(profile.specialty, self.specialty)
		self.assertEqual(profile.license_number, 'TEST-LICENSE-001')
