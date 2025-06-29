from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, OpenApiResponse

from events.serializers import EventSerializer, AttendeeSerializer, EventExpandSerializer
from events.models import Event


@extend_schema(
    tags=["Events"],
    description="API endpoint to manage events and register attendees."
)
class EventViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint to manage events and register attendees.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AttendeeSerializer,
        responses={
            201: OpenApiResponse(response=AttendeeSerializer, description="Attendee successfully registered."),
            400: OpenApiResponse(description="Validation error (e.g., event full, duplicate registration, etc.)"),
        },
        description="Register a user as an attendee to the specified event.",
        summary="Register attendee to event",
        tags=["Events"]
    )
    @action(
        detail=True,
        methods=['post'],
        url_path='register',
        serializer_class=AttendeeSerializer,
        permission_classes=[IsAuthenticated]
    )
    def register(self, request, pk=None):
        """
        Register an attendee for the specified event.

        Validation constraints (enforced in serializer):
        - Event creator cannot register as an attendee.
        - Same user cannot register more than once for the event.
        - Max capacity must not be exceeded.
        """
        # Get the event object
        event = self.get_object()

        # Pass event instance and request to serializer context
        serializer = self.get_serializer(
            data=request.data,
            context={
                'request': request,
                'event': event,
            }
        )

        # Validate data, raise 400 if invalid
        serializer.is_valid(raise_exception=True)

        # Save new attendee registration
        serializer.save()

        # Return created attendee data with HTTP 201
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        responses={
            200: OpenApiResponse(response=EventExpandSerializer, description="Event with its attendees"),
            404: OpenApiResponse(description="Event not found"),
        },
        summary="Get event with attendees",
        description="Returns detailed event info along with all registered attendees.",
        tags=["Events"]
    )
    @action(
        detail=True,
        methods=['get'],
        url_path='attendees',
        permission_classes=[IsAuthenticated]
    )
    def attendees(self, request, pk=None):
        """
        Retrieve detailed event information along with the list of registered attendees.
        """
        # Get the event object
        event = self.get_object()

        # Serialize event with expanded attendees info
        serializer = EventExpandSerializer(event)

        # Return serialized event data
        return Response(serializer.data, status=status.HTTP_200_OK)
