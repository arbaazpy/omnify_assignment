import factory
from faker import Faker
from datetime import timedelta
from django.utils import timezone

from events.models import Event, Attendee
from accounts.tests.factories import UserFactory

fake = Faker()


class EventFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Event instances with timezone-aware datetimes.
    """
    class Meta:
        model = Event

    creator = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda _: fake.sentence(nb_words=4))
    location = factory.LazyAttribute(lambda _: fake.city())

    start_time = factory.LazyFunction(
        lambda: timezone.make_aware(fake.future_datetime(end_date="+30d"))
    )
    end_time = factory.LazyAttribute(
        lambda o: o.start_time + timedelta(hours=2)
    )
    max_capacity = 10


class AttendeeFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Attendee instances.
    """
    class Meta:
        model = Attendee

    event = factory.SubFactory(EventFactory)
    user = factory.SubFactory(UserFactory)
