from django.test import TestCase

from api.constants import URGENCY_LEVELS
from api.models import StudyModel
from api.tests.factories import PatientFactory


class StudyModelTestCase(TestCase):
    def test_crud_study(self):
        # Create
        patient = PatientFactory()
        patient.save()
        urgency_level = URGENCY_LEVELS[0]
        study = StudyModel(urgency_level=urgency_level, patient=patient)

        # Read
        self.assertEqual(study.urgency_level, urgency_level)
        self.assertEqual(study.pk, study.id)
        self.assertEqual(study.patient.id, patient.id)

        # Update
        study.urgency_level = URGENCY_LEVELS[1]
        study.save()
        self.assertNotEqual(study.urgency_level, urgency_level)

        # Delete
        study_id = study.id
        study.delete()
        exists = StudyModel.objects.filter(pk=study_id).first()
        self.assertIsNone(exists)
