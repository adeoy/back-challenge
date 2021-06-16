from factory.django import DjangoModelFactory
from faker import Faker

from api.models import Patient

fake = Faker()


class PatientFactory(DjangoModelFactory):
    class Meta:
        model = Patient

    first_name = fake.first_name()
