import factory
from faker import Faker

from accounts.models import User


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating test User instances.
    """
    class Meta:
        model = User

    name = factory.LazyAttribute(lambda _: fake.name())
    email = factory.LazyAttribute(lambda _: fake.unique.email())

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        """
        Set password properly using Django's set_password method.
        """
        password = extracted or "TestPass123"
        obj.set_password(password)
        if create:
            obj.save()
