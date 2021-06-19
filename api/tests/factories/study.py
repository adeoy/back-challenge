import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from api.constants import STUDY_TYPES, URGENCY_LEVELS
from api.models import StudyModel
from api.tests.factories.patient import PatientFactory


class StudyFactory(DjangoModelFactory):
    class Meta:
        model = StudyModel

    urgency_level = factory.fuzzy.FuzzyChoice(URGENCY_LEVELS)
    body_part = factory.Faker("pystr")
    description = factory.Faker("pystr")
    type = factory.fuzzy.FuzzyChoice(STUDY_TYPES)
    patient = factory.SubFactory(PatientFactory)
    is_active = True
