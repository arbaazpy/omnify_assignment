from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating 
    'created_at' and 'updated_at' timestamp fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Event(TimeStampedModel):
    """
    Represents an event created by a user.

    Fields:
        - creator: ForeignKey to User who created the event.
        - name: Name of the event.
        - location: Location where the event will take place.
        - start_time: Date and time when the event starts.
        - end_time: Date and time when the event ends.
        - max_capacity: Maximum number of attendees allowed.
    """
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events'
    )
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"


class Attendee(TimeStampedModel):
    """
    Represents a user registered as an attendee for an event.

    Constraints:
        - A user can only register once per event.
        - A user cannot register for their own event (enforced in serializer).

    Fields:
        - event: The event the user is attending.
        - user: The user attending the event.
    """
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='attendees'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendees'
    )

    class Meta:
        unique_together = ('event', 'user')  # Prevent duplicate registrations

    def __str__(self):
        return f"{self.user.name} ({self.user.email}) for {self.event.name}"
