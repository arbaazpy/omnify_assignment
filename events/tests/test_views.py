from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from events.tests.factories import EventFactory, AttendeeFactory
from accounts.tests.factories import UserFactory
from accounts.models import User


class EventViewSetTests(APITestCase):
    """
    Test suite for the EventViewSet endpoints.
    """

    def setUp(self):
        self.user = UserFactory()
        self.user.set_password("testpass123")
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_create_event_success(self):
        url = reverse('event-list')
        data = {
            "name": "Omnify Event",
            "location": "Mumbai",
            "start_time": "2025-06-30T10:00:00Z",
            "end_time": "2099-06-30T12:00:00Z",
            "max_capacity": 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["creator"]["id"], self.user.id)

    def test_create_event_end_time_before_start_time(self):
        url = reverse('event-list')
        data = {
            "name": "Invalid Event",
            "location": "Delhi",
            "start_time": "2025-06-30T12:00:00Z",
            "end_time": "2025-06-30T10:00:00Z",
            "max_capacity": 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("End time must be after start time.", str(response.data))

    def test_list_events(self):
        EventFactory.create_batch(3, creator=self.user)
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        created_event_ids = set(EventFactory._meta.model.objects.filter(creator=self.user).values_list("id", flat=True))
        response_event_ids = set(event["id"] for event in results)
        self.assertTrue(created_event_ids.issubset(response_event_ids))


class AttendeeRegisterViewSetTests(APITestCase):
    """
    Test suite for the AttendeeRegisterViewSet endpoints.
    """

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_register_attendee_success(self):
        event = EventFactory(creator=self.user, max_capacity=2)
        other_user = UserFactory()
        url = reverse('register_attendee-list', kwargs={'event_id': event.id})
        response = self.client.post(url, {"user": other_user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], other_user.id)
        self.assertEqual(response.data["event"]["id"], event.id)

    def test_register_attendee_creator_fails(self):
        event = EventFactory(creator=self.user)
        url = reverse('register_attendee-list', kwargs={'event_id': event.id})
        response = self.client.post(url, {"user": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Event creator cannot register as an attendee", str(response.data))

    def test_register_attendee_duplicate_fails(self):
        event = EventFactory(max_capacity=2)
        attendee_user = UserFactory()
        AttendeeFactory(event=event, user=attendee_user)
        self.client.force_authenticate(user=attendee_user)
        url = reverse('register_attendee-list', kwargs={'event_id': event.id})
        response = self.client.post(url, {"user": attendee_user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already registered", str(response.data))

    def test_register_attendee_capacity_full_fails(self):
        event = EventFactory(max_capacity=1)
        user1 = UserFactory()
        user2 = UserFactory()
        AttendeeFactory(event=event, user=user1)
        self.client.force_authenticate(user=user2)
        url = reverse('register_attendee-list', kwargs={'event_id': event.id})
        response = self.client.post(url, {"user": user2.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Event is full", str(response.data))


class AttendeeListViewSetTests(APITestCase):
    """
    Test suite for the AttendeeListViewSet endpoints.
    """

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_event_attendees_list(self):
        event = EventFactory(creator=self.user)
        users = [UserFactory() for _ in range(3)]
        for user in users:
            AttendeeFactory(event=event, user=user)

        url = reverse('list_attendee-list', kwargs={'event_id': event.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        attendee_emails = [item['email'] for item in results if item['email'] in [u.email for u in users]]
        self.assertEqual(len(attendee_emails), 3)
        self.assertEqual(sorted(attendee_emails), sorted([u.email for u in users]))
