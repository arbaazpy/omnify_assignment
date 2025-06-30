from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from django.shortcuts import get_object_or_404

from accounts.serializers import UserSerializer
from accounts.models import User
from events.serializers import EventSerializer, AttendeeSerializer
from events.models import Event, Attendee


@extend_schema(
    tags=["Events"],
    description="API endpoint to manage events."
)
class EventViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    API endpoint to manage events.
    Supports listing and creation of events by authenticated users.
    Automatically associates the authenticated user as the creator.
    """
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["Attendees"],
    description="API endpoint to register attendees for an event."
)
class AttendeeRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint to register an attendee for a specific event.
    Enforces constraints such as duplicate registration, max capacity, and creator restriction.
    """
    serializer_class = AttendeeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Attendee.objects.all()


@extend_schema(
    tags=["Attendees"],
    description="API endpoint to list attendees for an event."
)
class AttendeeListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint to list all registered users (attendees) for a specific event.
    Returns a list of user profiles associated with that event.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().prefetch_related('attendees').order_by('id')

    def get_queryset(self):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        return super().get_queryset().filter(attendees__event_id=event.id)
