from django.test import TestCase

from api.models import PatientModel
from api.tests.factories import PatientFactory


class PatientModelTestCase(TestCase):
    def test_crud_patient(self):
        # Create
        first_name = "Héctor Hugo"
        patient = PatientFactory(first_name=first_name)

        # Read
        self.assertEqual(patient.first_name, first_name)
        self.assertEqual(patient.pk, patient.id)

        # Update
        patient.first_name = "José Martín"
        patient.save()
        self.assertNotEqual(patient.first_name, first_name)

        # Delete
        patient_id = patient.id
        patient.delete()
        exists = PatientModel.objects.filter(pk=patient_id).first()
        self.assertIsNone(exists)
