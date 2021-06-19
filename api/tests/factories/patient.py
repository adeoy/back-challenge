import factory
from factory.django import DjangoModelFactory

from api.models import PatientModel


class PatientFactory(DjangoModelFactory):
    class Meta:
        model = PatientModel

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birth_date = factory.Faker("date")
    email = factory.Faker("email")
    is_active = True
