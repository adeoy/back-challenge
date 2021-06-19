from typing import List, Optional

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.models import PatientModel
from api.serializers import PatientSerializer


class PatientViewSet(ViewSet):
    """
    List Patients View

    Methods:
    GET (list): Returns the patients list
    GET (detail): Return a patient
    POST: Create a new patient
    PUT: Update a patient
    PATCH: Update only the received fields of a patient
    DELETE: Delete a patient
    """

    serializer_class = PatientSerializer
    queryset = PatientModel.objects.all()

    def list(self, request: Request) -> Response:
        """Return a list of all Patients

        Query params:
        only-active (int): Set 1 to filter only active (not deleted) patients and 0 for all

        Returns:
        list: List of patients json object
        """
        only_active = request.query_params.get("only-active", "1") == "1"
        if only_active:
            patients: List[PatientModel] = PatientModel.objects.filter(
                is_active=only_active
            )
        else:
            patients = self.queryset
        serializer = self.serializer_class(patients, many=True)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        """Create a new patient

        Body params:
        first_name (str): Patient first name,
        last_name (str): Patient last name,
        birth_date (str): Patient birth date (formar "YYYY-MM-DD"),
        email (str): Patient email

        Returns:
        int: ID of the new created patient
        """
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"id": serializer.instance.id}, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, pk: Optional[int] = None) -> Response:
        """Return a single patient by its ID

        In-Url params:
        patient_id (int): Patient ID to retrieve

        Returns:
        dict: Patient details object
        """
        patient: PatientModel = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: Optional[int] = None) -> Response:
        """Update a patient fields

        In-Url params:
        patient_id (int): Patient ID to update

        Body params:
        first_name (str): Patient first name,
        last_name (str): Patient last name,
        birth_date (str): Patient birth date (formar "YYYY-MM-DD"),
        email (str): Patient email

        Returns:
        int: ID of the updated patient
        """
        patient: PatientModel = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(patient, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"id": pk}, status=status.HTTP_200_OK)

    def partial_update(self, request: Request, pk: Optional[int] = None) -> Response:
        """Update only the received patient fields

        In-Url params:
        patient_id (int): Patient ID to update

        Body params:
        first_name (str): Patient first name,
        last_name (str): Patient last name,
        birth_date (str): Patient birth date (formar "YYYY-MM-DD"),
        email (str): Patient email

        Returns:
        int: ID of the updated patient
        """
        patient: PatientModel = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(patient, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"id": pk}, status=status.HTTP_200_OK)

    def destroy(self, request: Request, pk: Optional[int] = None) -> Response:
        """Delete a patient by its ID

        In-Url params:
        patient_id (int): Patient ID to delete

        Returns:
        int: ID of the deleted patient
        """
        patient: PatientModel = get_object_or_404(self.queryset, pk=pk, is_active=True)
        patient.is_active = False
        patient.save()
        return Response({"id": pk}, status=status.HTTP_200_OK)
