from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from django.shortcuts import get_object_or_404

from accounts.serializers import UserSerializer
from accounts.models import User
from events.serializers import EventSerializer, AttendeeSerializer
from events.models import Event, Attendee


@extend_schema(
    tags=["Events"],
    description="API endpoint to manage events. Optional timezone support via ?tz=Europe/London.",
    parameters=[
        OpenApiParameter(
            name='tz',
            description='Optional timezone string (e.g., Asia/Kolkata, Europe/London)',
            required=False,
            type=str,
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(
                    name='India Timezone',
                    value='Asia/Kolkata',
                    summary='Convert datetimes to India Standard Time'
                ),
                OpenApiExample(
                    name='UK Timezone',
                    value='Europe/London',
                    summary='Convert datetimes to UK time'
                ),
                 OpenApiExample(
                    name='US (Eastern) Timezone',
                    value='America/New_York',
                    summary='Convert datetimes to US time'
                )
            ]
        )
    ]
)
class EventViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    API endpoint to manage events.

    Features:
    - Authenticated users can list and create events.
    - Automatically associates the authenticated user as the event creator.
    - Supports optional timezone conversion for datetime fields via the `tz` query parameter (e.g., ?tz=Europe/London).
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
