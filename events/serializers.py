from django.contrib.auth import get_user_model

from rest_framework import serializers

from accounts.serializers import UserSerializer
from events.models import Event, Attendee


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model.
    Sets creator to the authenticated user from request context.
    Validates that end_time is after start_time.
    """
    creator = UserSerializer(read_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data['creator'] = self.context['view'].request.user
        if validated_data['end_time'] <= validated_data['start_time']:
            raise serializers.ValidationError('End time must be after start time.')
        return validated_data

    class Meta:
        model = Event
        fields = [
            'id', 'creator', 'name', 'location', 'start_time', 'end_time',
            'max_capacity', 'created_at', 'updated_at'
        ]


class AttendeeSerializer(serializers.ModelSerializer):
    """
    Serializer for registering an attendee to an event.
    Enforces the following:
    - Event creator cannot register as attendee.
    - User cannot register more than once for the same event.
    - Event must not exceed its max capacity.
    """
    event = EventSerializer(read_only=True)

    def validate(self, attrs):
        # First, run parent validation chain
        attrs = super().validate(attrs)

        event = self.context['event']
        user = attrs['user']
        attrs['event'] = event

        # Event creator cannot be an attendee
        if user == event.creator:
            raise serializers.ValidationError("Event creator cannot register as an attendee.")

        # Prevent duplicate registrations
        if event.attendees.filter(user=user).exists():
            raise serializers.ValidationError("This user is already registered for the event.")

        # Enforce capacity limits
        if event.attendees.count() >= event.max_capacity:
            raise serializers.ValidationError("Event is full. Max capacity reached.")

        return attrs

    class Meta:
        model = Attendee
        fields = ['id', 'event', 'user', 'created_at', 'updated_at']
        read_only_fields = ['event', 'created_at', 'updated_at']


class EventExpandSerializer(serializers.ModelSerializer):
    """
    Serializer that includes event details plus a flat list of attendee users.
    """
    creator = UserSerializer(read_only=True)
    attendees = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'location',
            'start_time',
            'end_time',
            'max_capacity',
            'creator',
            'attendees',
            'created_at',
            'updated_at'
        ]

    def get_attendees(self, obj):
        """
        Return a flat list of users who are registered attendees for this event.
        """
        users = [attendee.user for attendee in obj.attendees.all()]
        return UserSerializer(users, many=True).data
