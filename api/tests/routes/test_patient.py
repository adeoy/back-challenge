from rest_framework import status
from rest_framework.test import APITestCase

from api.models import PatientModel
from api.tests.factories import PatientFactory


class PatientTests(APITestCase):
    def setUp(self) -> None:
        PatientFactory.create_batch(5)
        self.patient: PatientModel = PatientModel.objects.first()
        self.api_url = "/api/patients"

    def test_list_patient(self):
        """
        Test the list of patients
        """
        response = self.client.get(f"{self.api_url}/?format=json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PatientModel.objects.count(), 5)

    def test_retrieve_patient(self):
        """
        Test the retrieve of one patient
        """

        response = self.client.get(f"{self.api_url}/{self.patient.id}/?format=json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertEqual(self.patient.first_name, data["first_name"])

    def test_create_patient(self):
        """
        Test the create a patient
        """
        payload = {
            "first_name": "Mario",
            "last_name": "Rodríguez",
            "birth_date": "1972-05-24",
            "email": "mario@gmail.com",
            "is_active": True,
        }

        # Happy path!
        response = self.client.post(f"{self.api_url}/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["id"], int)

        # Non unique email
        response = self.client.post(f"{self.api_url}/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["email"], list)
        self.assertEqual(data["email"][0], "This field must be unique.")

        # Bad date
        payload["birth_date"] = "invalid"
        response = self.client.post(f"{self.api_url}/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["birth_date"], list)
        self.assertIn("Date has wrong format", data["birth_date"][0])

        # Missing field
        payload.pop("first_name")
        response = self.client.post(f"{self.api_url}/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["first_name"], list)
        self.assertEqual(data["first_name"][0], "This field is required.")

    def test_update_patient(self):
        """
        Test the update a patient
        """

        old_first_name: str = self.patient.first_name
        payload = {
            "first_name": "Lucio",
            "last_name": "Sánchez",
            "birth_date": "1987-03-12",
            "email": "lucio@gmail.com",
            "is_active": True,
        }

        # Happy path!
        response = self.client.put(
            f"{self.api_url}/{self.patient.id}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.patient.refresh_from_db()
        self.assertNotEqual(self.patient.first_name, old_first_name)

        # Missing field
        payload.pop("first_name")
        response = self.client.put(
            f"{self.api_url}/{self.patient.id}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["first_name"], list)
        self.assertEqual(data["first_name"][0], "This field is required.")

    def test_partially_update_patient(self):
        """
        Test the partial update a patient
        """

        old_first_name: str = self.patient.first_name
        payload = {
            "first_name": "Juan",
        }

        # Happy path!
        response = self.client.patch(
            f"{self.api_url}/{self.patient.id}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient.refresh_from_db()
        self.assertNotEqual(self.patient.first_name, old_first_name)

    def test_delete_patient(self):
        """
        Test the delete a patient
        """
        # Happy path!
        response = self.client.delete(f"{self.api_url}/{self.patient.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.is_active, False)
