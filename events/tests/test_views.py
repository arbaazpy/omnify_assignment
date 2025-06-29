from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from events.models import Event, Attendee
from events.tests.factories import EventFactory, AttendeeFactory
from accounts.tests.factories import UserFactory


class EventViewSetTests(APITestCase):
    """
    Test suite for the EventViewSet endpoints.
    """

    def setUp(self):
        """
        Setup test users and authentication.
        """
        self.user = UserFactory()
        self.user.set_password("testpass123")
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_create_event_success(self):
        """
        Ensure authenticated users can create events.
        """
        url = reverse('event-list')
        data = {
            "name": "Conference 2025",
            "location": "Berlin",
            "start_time": "2099-01-01T10:00:00Z",
            "end_time": "2099-01-01T12:00:00Z",
            "max_capacity": 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["creator"]["id"], self.user.id)

    def test_register_attendee_success(self):
        """
        User can register another user as attendee for an event.
        """
        event = EventFactory(creator=self.user, max_capacity=2)
        other_user = UserFactory()
        url = reverse('event-register', kwargs={'pk': event.id})
        data = {"user": other_user.id}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], other_user.id)
        self.assertEqual(response.data["event"]["id"], event.id)

    def test_register_attendee_creator_fails(self):
        """
        Event creator cannot register as an attendee.
        """
        event = EventFactory(creator=self.user)
        url = reverse('event-register', kwargs={'pk': event.id})
        data = {"user": self.user.id}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Event creator cannot register as an attendee", str(response.data))

    def test_register_duplicate_attendee_fails(self):
        """
        Same user cannot register twice for the same event.
        """
        event = EventFactory(max_capacity=2)
        attendee_user = UserFactory()
        AttendeeFactory(event=event, user=attendee_user)

        self.client.force_authenticate(user=attendee_user)
        url = reverse('event-register', kwargs={'pk': event.id})
        data = {"user": attendee_user.id}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already registered", str(response.data))

    def test_register_attendee_capacity_full_fails(self):
        """
        Should not register if event is at full capacity.
        """
        event = EventFactory(max_capacity=1)
        user1 = UserFactory()
        user2 = UserFactory()

        AttendeeFactory(event=event, user=user1)
        self.client.force_authenticate(user=user2)

        url = reverse('event-register', kwargs={'pk': event.id})
        data = {"user": user2.id}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Event is full", str(response.data))

    def test_event_attendees_list(self):
        """
        Return event details with all registered attendees.
        """
        event = EventFactory(creator=self.user)
        users = [UserFactory() for _ in range(3)]
        for user in users:
            AttendeeFactory(event=event, user=user)

        url = reverse('event-attendees', kwargs={'pk': event.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["attendees"]), 3)

        attendee_emails = [u["email"] for u in response.data["attendees"]]
        for u in users:
            self.assertIn(u.email, attendee_emails)
