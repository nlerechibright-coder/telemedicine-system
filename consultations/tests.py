from django.contrib.auth import get_user_model
from django.test import TestCase

from doctors.models import DoctorProfile, Specialty
from episodes.models import DoctorRequest, HealthEpisode
from messaging.models import ChatMessage, ChatRoom
from messaging.utils import can_access_chat


class ConsultationRequestFlowTests(TestCase):
	def setUp(self):
		user_model = get_user_model()
		self.client_user = user_model.objects.create_user(
			email='client@example.com',
			password='password',
			role=user_model.Role.CLIENT,
		)
		self.doctor_user = user_model.objects.create_user(
			email='doctor@example.com',
			password='password',
			role=user_model.Role.DOCTOR,
		)
		self.other_doctor = user_model.objects.create_user(
			email='other-doctor@example.com',
			password='password',
			role=user_model.Role.DOCTOR,
		)
		specialty = Specialty.objects.create(name='General Practice')
		DoctorProfile.objects.create(
			user=self.doctor_user,
			specialty=specialty,
			license_number='TEST-001',
			qualifications='MD',
			consultation_fee=0,
			is_verified=True,
		)
		DoctorProfile.objects.create(
			user=self.other_doctor,
			specialty=specialty,
			license_number='TEST-002',
			qualifications='MD',
			consultation_fee=0,
			is_verified=True,
		)

	def test_existing_doctor_submission_uses_new_persistent_flow(self):
		self.client.force_login(self.client_user)
		response = self.client.post(
			'/consultations/request/',
			{
				'doctor': self.doctor_user.id,
				'reason': 'Need a consultation',
				'scheduled_at': '',
			},
		)

		self.assertEqual(response.status_code, 302)
		doctor_request = DoctorRequest.objects.get()
		self.assertEqual(doctor_request.doctor_id, self.doctor_user.id)
		self.assertEqual(doctor_request.client_id, self.client_user.id)
		self.assertEqual(doctor_request.status, DoctorRequest.Status.PENDING)
		self.assertEqual(doctor_request.episode.status, HealthEpisode.Status.AWAITING_DOCTOR)

		self.client.force_login(self.doctor_user)
		dashboard_response = self.client.get('/doctors/dashboard/')
		self.assertContains(dashboard_response, f'Request #{doctor_request.id}')

		self.client.force_login(self.other_doctor)
		other_dashboard_response = self.client.get('/doctors/dashboard/')
		self.assertNotContains(other_dashboard_response, f'Request #{doctor_request.id}')

		self.client.force_login(self.doctor_user)
		response = self.client.post(
			f'/episodes/doctor/requests/{doctor_request.id}/',
			{'status': DoctorRequest.Status.ACCEPTED, 'doctor_notes': '', 'rejection_reason': ''},
		)

		self.assertEqual(response.status_code, 302)
		doctor_request.refresh_from_db()
		doctor_request.episode.refresh_from_db()
		self.assertEqual(doctor_request.status, DoctorRequest.Status.ACCEPTED)
		self.assertEqual(doctor_request.episode.status, HealthEpisode.Status.IN_CONSULTATION)
		self.assertEqual(ChatRoom.objects.filter(episode=doctor_request.episode).count(), 1)
		self.assertTrue(can_access_chat(self.client_user, doctor_request.episode))
		self.assertTrue(can_access_chat(self.doctor_user, doctor_request.episode))
		self.assertFalse(can_access_chat(self.other_doctor, doctor_request.episode))

		room = ChatRoom.objects.get(episode=doctor_request.episode)
		ChatMessage.objects.create(room=room, sender=self.client_user, content='Hello doctor')
		self.assertEqual(ChatRoom.objects.get(episode=doctor_request.episode).messages.count(), 1)
		self.assertEqual(HealthEpisode.objects.count(), 1)

# Create your tests here.
