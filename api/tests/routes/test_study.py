from typing import List

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import PatientModel, StudyModel
from api.tests.factories import PatientFactory, StudyFactory


class StudyTests(APITestCase):
    def setUp(self) -> None:
        patients: List[PatientModel] = PatientFactory.create_batch(5)
        StudyFactory.create_batch(5, patient=patients[0])
        StudyFactory.create_batch(3, patient=patients[1])

        self.patient1_id: int = patients[0].id
        self.patient2_id: int = patients[1].id

        self.patient1_study: StudyModel = StudyModel.objects.filter(
            patient__pk=self.patient1_id
        ).first()

        self.api_url = f"/api/patients"

    def test_list_study(self):
        """
        Test the list of studies
        """
        response = self.client.get(
            f"{self.api_url}/{self.patient1_id}/studies/?format=json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            StudyModel.objects.filter(patient__pk=self.patient1_id).count(), 5
        )

        response = self.client.get(
            f"{self.api_url}/{self.patient2_id}/studies/?format=json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            StudyModel.objects.filter(patient__pk=self.patient2_id).count(), 3
        )

    def test_retrieve_study(self):
        """
        Test the retrieve of one study
        """

        response = self.client.get(
            f"{self.api_url}/{self.patient1_id}/studies/{self.patient1_study.id}/?format=json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertEqual(self.patient1_study.urgency_level, data["urgency_level"])

    def test_create_study(self):
        """
        Test the create a study
        """
        payload = {
            "urgency_level": "LOW",
            "body_part": "HEAD",
            "description": "INFLAMATION",
            "type": "XRAY",
            "is_active": True,
        }

        # Happy path!
        response = self.client.post(
            f"{self.api_url}/{self.patient1_id}/studies/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["id"], int)

        # Urgency level only LOW, MED, HIGH
        # Type only XRAY, MAMMOGRAM
        payload["urgency_level"] = "invalid"
        payload["type"] = "invalid"
        response = self.client.post(
            f"{self.api_url}/{self.patient1_id}/studies/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["urgency_level"], list)
        self.assertIn("is not a valid choice.", data["urgency_level"][0])
        self.assertIsInstance(data["type"], list)
        self.assertIn("is not a valid choice.", data["type"][0])

        # Missing field
        payload.pop("description")
        response = self.client.post(
            f"{self.api_url}/{self.patient1_id}/studies/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["description"], list)
        self.assertEqual(data["description"][0], "This field is required.")

    def test_update_study(self):
        """
        Test the update a study
        """

        description: str = self.patient1_study.description
        payload = {
            "urgency_level": "LOW",
            "body_part": "HEAD",
            "description": "INFLAMATION",
            "type": "XRAY",
            "is_active": True,
        }

        # Happy path!
        response = self.client.put(
            f"{self.api_url}/{self.patient1_id}/studies/{self.patient1_study.id}/",
            payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.patient1_study.refresh_from_db()
        self.assertNotEqual(self.patient1_study.description, description)

        # Missing field
        payload.pop("description")
        response = self.client.put(
            f"{self.api_url}/{self.patient1_id}/studies/{self.patient1_study.id}/",
            payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data["description"], list)
        self.assertEqual(data["description"][0], "This field is required.")

    def test_partially_update_study(self):
        """
        Test the partial update a study
        """

        description: str = self.patient1_study.description
        payload = {
            "description": "PAIN IN KNEE",
        }

        # Happy path!
        response = self.client.patch(
            f"{self.api_url}/{self.patient1_id}/studies/{self.patient1_study.id}/",
            payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient1_study.refresh_from_db()
        self.assertNotEqual(self.patient1_study.description, description)

    def test_delete_study(self):
        """
        Test the delete a study
        """
        # Happy path!
        response = self.client.delete(
            f"{self.api_url}/{self.patient1_id}/studies/{self.patient1_study.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient1_study.refresh_from_db()
        self.assertEqual(self.patient1_study.is_active, False)
