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
        if attrs['end_time'] <= attrs['start_time']:
            raise serializers.ValidationError('End time must be after start time.')
        return attrs

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

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
        attrs = super().validate(attrs)

        event_id = self.context['view'].kwargs['event_id']
        try:
            event = Event.objects.prefetch_related('attendees__user').get(id=event_id)
        except Event.DoesNotExist as e:
            raise serializers.ValidationError("Event does not exist.") from e

        user = attrs['user']
        attrs['event'] = event

        if user == event.creator:
            raise serializers.ValidationError("Event creator cannot register as an attendee.")

        if event.attendees.filter(user=user).exists():
            raise serializers.ValidationError("This user is already registered for the event.")

        if event.attendees.count() >= event.max_capacity:
            raise serializers.ValidationError("Event is full. Max capacity reached.")

        return attrs

    class Meta:
        model = Attendee
        fields = ['id', 'event', 'user', 'created_at', 'updated_at']
        read_only_fields = ['event', 'created_at', 'updated_at']
