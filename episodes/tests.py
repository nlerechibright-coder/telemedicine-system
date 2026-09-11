from django.contrib.auth import get_user_model
from django.test import TestCase

from doctors.models import DoctorProfile, Specialty
from messaging.models import ChatMessage, ChatRoom
from messaging.utils import can_access_chat
from .models import DoctorRequest, HealthEpisode


class ConsultationRequestRegressionTests(TestCase):
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
		self.episode = HealthEpisode.objects.create(
			client=self.client_user,
			title='Request regression episode',
			status=HealthEpisode.Status.MATCHING,
		)

	def test_selected_doctor_receives_request_and_chat_persists_after_acceptance(self):
		self.client.force_login(self.client_user)
		response = self.client.post(
			f'/episodes/{self.episode.id}/request-doctor/',
			{'doctor': self.doctor_user.id, 'reason': 'Need a consultation'},
		)

		self.assertEqual(response.status_code, 302)
		doctor_request = DoctorRequest.objects.get(episode=self.episode)
		self.assertEqual(doctor_request.doctor, self.doctor_user)
		self.assertEqual(doctor_request.status, DoctorRequest.Status.PENDING)
		self.assertEqual(doctor_request.episode.status, HealthEpisode.Status.AWAITING_DOCTOR)

		self.client.force_login(self.doctor_user)
		dashboard_response = self.client.get('/doctors/dashboard/')
		self.assertEqual(dashboard_response.status_code, 200)
		self.assertContains(dashboard_response, f'Request #{doctor_request.id}')

		pending_response = self.client.get('/episodes/doctor/pending/')
		self.assertContains(pending_response, f'Request #{doctor_request.id}')

		self.client.force_login(self.other_doctor)
		other_dashboard_response = self.client.get('/doctors/dashboard/')
		self.assertNotContains(other_dashboard_response, f'Request #{doctor_request.id}')
		other_pending_response = self.client.get('/episodes/doctor/pending/')
		self.assertNotContains(other_pending_response, f'Request #{doctor_request.id}')

		self.client.force_login(self.doctor_user)
		response = self.client.post(
			f'/episodes/doctor/requests/{doctor_request.id}/',
			{'status': DoctorRequest.Status.ACCEPTED, 'doctor_notes': '', 'rejection_reason': ''},
		)

		self.assertEqual(response.status_code, 302)
		doctor_request.refresh_from_db()
		self.episode.refresh_from_db()
		self.assertEqual(doctor_request.status, DoctorRequest.Status.ACCEPTED)
		self.assertEqual(doctor_request.doctor, self.doctor_user)
		self.assertEqual(self.episode.status, HealthEpisode.Status.IN_CONSULTATION)
		self.assertEqual(ChatRoom.objects.filter(episode=self.episode).count(), 1)
		self.assertTrue(can_access_chat(self.client_user, self.episode))
		self.assertTrue(can_access_chat(self.doctor_user, self.episode))
		self.assertFalse(can_access_chat(self.other_doctor, self.episode))

		room = ChatRoom.objects.get(episode=self.episode)
		ChatMessage.objects.create(room=room, sender=self.client_user, content='Hello doctor')
		self.assertEqual(ChatRoom.objects.get(episode=self.episode).messages.count(), 1)

# Create your tests here.
