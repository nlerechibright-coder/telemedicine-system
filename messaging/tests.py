from django.contrib.auth import get_user_model
from django.test import TestCase

from doctors.models import DoctorProfile, Specialty
from episodes.models import DoctorRequest, HealthEpisode
from messaging.models import ChatMessage, ChatRoom
from clients.models import ClientProfile
from messaging.utils import can_access_chat
from messaging.video import build_whatsapp_link, normalize_whatsapp_number


class ChatRoomPersistenceTests(TestCase):
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
		specialty = Specialty.objects.create(name='General Practice')
		DoctorProfile.objects.create(
			user=self.doctor_user,
			specialty=specialty,
			license_number='TEST-001',
			qualifications='MD',
			consultation_fee=0,
			is_verified=True,
		)
		self.episode = HealthEpisode.objects.create(
			client=self.client_user,
			title='Persistent episode',
			status=HealthEpisode.Status.AWAITING_DOCTOR,
		)
		self.request = DoctorRequest.objects.create(
			episode=self.episode,
			client=self.client_user,
			doctor=self.doctor_user,
			reason='Need advice',
		)

	def test_acceptance_creates_one_room_and_messages_survive_retrieval(self):
		self.request.status = DoctorRequest.Status.ACCEPTED
		self.request.save()

		self.assertEqual(ChatRoom.objects.filter(episode=self.episode).count(), 1)
		room = ChatRoom.objects.get(episode=self.episode)
		self.assertEqual(room.episode_id, self.episode.id)
		self.assertTrue(can_access_chat(self.client_user, self.episode))
		self.assertTrue(can_access_chat(self.doctor_user, self.episode))

		ChatMessage.objects.create(room=room, sender=self.client_user, content='Hello doctor')
		ChatMessage.objects.create(room=room, sender=self.doctor_user, content='Hello client')
		self.assertEqual(room.messages.count(), 2)

		self.request.save()
		self.assertEqual(ChatRoom.objects.filter(episode=self.episode).count(), 1)
		self.assertEqual(ChatRoom.objects.get(episode=self.episode).messages.count(), 2)


class WhatsAppVideoConsultationTests(TestCase):
	def setUp(self):
		user_model = get_user_model()
		self.client_user = user_model.objects.create_user(
			email='video-client@example.com',
			password='password',
			role=user_model.Role.CLIENT,
		)
		self.other_client = user_model.objects.create_user(
			email='other-client@example.com',
			password='password',
			role=user_model.Role.CLIENT,
		)
		self.doctor_user = user_model.objects.create_user(
			email='video-doctor@example.com',
			password='password',
			role=user_model.Role.DOCTOR,
		)
		self.other_doctor = user_model.objects.create_user(
			email='other-video-doctor@example.com',
			password='password',
			role=user_model.Role.DOCTOR,
		)
		specialty = Specialty.objects.create(name='Video Practice')
		DoctorProfile.objects.create(
			user=self.doctor_user,
			specialty=specialty,
			license_number='VIDEO-001',
			qualifications='MD',
			consultation_fee=0,
			whatsapp_number='08029011944',
			is_verified=True,
		)
		DoctorProfile.objects.create(
			user=self.other_doctor,
			specialty=specialty,
			license_number='VIDEO-002',
			qualifications='MD',
			consultation_fee=0,
			is_verified=True,
		)
		ClientProfile.objects.create(
			user=self.client_user,
			full_name='Video Client',
			date_of_birth='1990-01-01',
			gender=ClientProfile.Gender.OTHER,
			phone_number='08000000000',
			whatsapp_number='08031112222',
			blood_type=ClientProfile.BloodType.UNKNOWN,
		)
		ClientProfile.objects.create(
			user=self.other_client,
			full_name='Other Client',
			date_of_birth='1990-01-01',
			gender=ClientProfile.Gender.OTHER,
			phone_number='08000000001',
			whatsapp_number='08033334444',
			blood_type=ClientProfile.BloodType.UNKNOWN,
		)
		self.episode = HealthEpisode.objects.create(
			client=self.client_user,
			title='Video episode',
			status=HealthEpisode.Status.AWAITING_DOCTOR,
		)
		self.request = DoctorRequest.objects.create(
			episode=self.episode,
			client=self.client_user,
			doctor=self.doctor_user,
			reason='Need a video consultation',
		)

	def accept_request(self):
		self.request.status = DoctorRequest.Status.ACCEPTED
		self.request.save()

	def test_nigerian_number_and_provider_url(self):
		self.assertEqual(normalize_whatsapp_number('08029011944'), '2348029011944')
		self.assertEqual(
			build_whatsapp_link('08029011944', 'Hello doctor'),
			'https://wa.me/2348029011944?text=Hello+doctor',
		)

	def test_client_and_assigned_doctor_can_start_video_for_active_episode(self):
		self.accept_request()

		self.client.force_login(self.client_user)
		client_response = self.client.get(f'/messaging/episode/{self.episode.id}/start-video/')
		self.assertEqual(client_response.status_code, 302)
		self.assertIn('https://wa.me/2348029011944', client_response.url)

		self.client.force_login(self.doctor_user)
		doctor_response = self.client.get(f'/messaging/episode/{self.episode.id}/start-video/')
		self.assertEqual(doctor_response.status_code, 302)
		self.assertIn('https://wa.me/2348031112222', doctor_response.url)

		self.episode.refresh_from_db()
		self.assertIsNotNone(self.episode.video_started_at)

	def test_pending_completed_and_unrelated_users_cannot_start_video(self):
		self.client.force_login(self.client_user)
		pending_response = self.client.get(f'/messaging/episode/{self.episode.id}/start-video/')
		self.assertEqual(pending_response.status_code, 302)
		self.assertNotIn('wa.me', pending_response.url)
		self.episode.refresh_from_db()
		self.assertIsNone(self.episode.video_started_at)

		self.client.force_login(self.other_doctor)
		self.assertEqual(
			self.client.get(f'/messaging/episode/{self.episode.id}/start-video/').status_code,
			403,
		)

		self.client.force_login(self.other_client)
		self.assertEqual(
			self.client.get(f'/messaging/episode/{self.episode.id}/start-video/').status_code,
			403,
		)

		self.accept_request()
		self.episode.status = HealthEpisode.Status.COMPLETED
		self.episode.save()
		self.client.force_login(self.client_user)
		completed_response = self.client.get(f'/messaging/episode/{self.episode.id}/start-video/')
		self.assertEqual(completed_response.status_code, 302)
		self.assertNotIn('wa.me', completed_response.url)

	def test_missing_whatsapp_number_is_safe(self):
		self.doctor_user.doctor_profile.whatsapp_number = ''
		self.doctor_user.doctor_profile.save(update_fields=['whatsapp_number'])
		self.accept_request()

		self.client.force_login(self.client_user)
		response = self.client.get(f'/messaging/episode/{self.episode.id}/start-video/')
		self.assertEqual(response.status_code, 302)
		self.assertNotIn('wa.me', response.url)
		self.assertTrue(
			any('WhatsApp contact number has not been configured' in message.message for message in response.wsgi_request._messages)
		)

		self.client_user.client_profile.whatsapp_number = ''
		self.client_user.client_profile.save(update_fields=['whatsapp_number'])
		self.client.force_login(self.doctor_user)
		doctor_response = self.client.get(f'/messaging/episode/{self.episode.id}/start-video/')
		self.assertEqual(doctor_response.status_code, 302)
		self.assertNotIn('wa.me', doctor_response.url)

	def test_chat_room_and_messages_remain_persistent(self):
		self.accept_request()
		room = ChatRoom.objects.get(episode=self.episode)
		ChatMessage.objects.create(room=room, sender=self.client_user, content='Ready for video')
		self.client.force_login(self.client_user)
		self.assertEqual(self.client.get(f'/messaging/episode/{self.episode.id}/').status_code, 200)
		self.assertEqual(ChatRoom.objects.get(episode=self.episode).messages.count(), 1)
