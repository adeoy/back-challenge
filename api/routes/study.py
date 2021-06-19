from typing import List, Optional

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.models import StudyModel
from api.serializers import StudySerializer


class StudyViewSet(ViewSet):
    """
    List Studies View

    Methods:
    GET (list): Returns the studies list
    GET (detail): Return a study
    POST: Create a new study
    PUT: Update a study
    PATCH: Update only the received fields of a study
    DELETE: Delete a study
    """

    serializer_class = StudySerializer
    queryset = StudyModel.objects.all()

    def list(self, request: Request, patient_pk: Optional[int] = None) -> Response:
        """Return a list of all Studies

        Query params:
        only-active (int): Set 1 to filter only active (not deleted) studies and 0 for all

        Returns:
        list: List of studies json object
        """
        only_active = request.query_params.get("only-active", "1") == "1"
        if only_active:
            studies: List[StudyModel] = StudyModel.objects.filter(
                patient__pk=patient_pk, is_active=only_active
            )
        else:
            studies: List[StudyModel] = StudyModel.objects.filter(
                patient__pk=patient_pk
            )
        serializer = self.serializer_class(studies, many=True)
        return Response(serializer.data)

    def create(self, request: Request, patient_pk: Optional[int] = None) -> Response:
        """Create a new study

        In-Url params:
        patient_id (int): Patient ID of the current study

        Body params:
        urgency_level (str): Study urgency level (LOW, MID, HIGH)
        body_part (str): Study body part
        description (str): Study description
        type (str): Study type (XRAY, MAMMOGRAM)

        Returns:
        int: ID of the new created study
        """
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(patient_id=patient_pk)
        return Response({"id": serializer.instance.id}, status=status.HTTP_201_CREATED)

    def retrieve(
        self,
        request: Request,
        pk: Optional[int] = None,
        patient_pk: Optional[int] = None,
    ) -> Response:
        """Return a single study by its ID

        In-Url params:
        patient_id (int): Patient ID of the current study
        study_id (int): Study ID to retrieve

        Returns:
        dict: Study details object
        """
        study: StudyModel = get_object_or_404(
            self.queryset, pk=pk, patient__pk=patient_pk
        )
        serializer = self.serializer_class(study)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(
        self,
        request: Request,
        pk: Optional[int] = None,
        patient_pk: Optional[int] = None,
    ) -> Response:
        """Update a study fields

        In-Url params:
        patient_id (int): Patient ID of the current study
        study_id (int): Study ID to retrieve

        Body params:
        urgency_level (str): Study urgency level (LOW, MID, HIGH)
        body_part (str): Study body part
        description (str): Study description
        type (str): Study type (XRAY, MAMMOGRAM)

        Returns:
        int: ID of the updated study
        """
        study: StudyModel = get_object_or_404(
            self.queryset, pk=pk, patient__pk=patient_pk
        )
        serializer = self.serializer_class(study, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"id": pk}, status=status.HTTP_200_OK)

    def partial_update(
        self,
        request: Request,
        pk: Optional[int] = None,
        patient_pk: Optional[int] = None,
    ) -> Response:
        """Update only the received study fields

        In-Url params:
        patient_id (int): Patient ID of the current study
        study_id (int): Study ID to retrieve

        Body params:
        urgency_level (str): Study urgency level (LOW, MID, HIGH)
        body_part (str): Study body part
        description (str): Study description
        type (str): Study type (XRAY, MAMMOGRAM)

        Returns:
        int: ID of the updated study
        """
        study: StudyModel = get_object_or_404(
            self.queryset, pk=pk, patient__pk=patient_pk
        )
        serializer = self.serializer_class(study, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"id": pk}, status=status.HTTP_200_OK)

    def destroy(
        self,
        request: Request,
        pk: Optional[int] = None,
        patient_pk: Optional[int] = None,
    ) -> Response:
        """Delete a study by its ID

        In-Url params:
        patient_id (int): Patient ID of the current study
        study_id (int): Study ID to retrieve

        Returns:
        int: ID of the deleted study
        """
        study: StudyModel = get_object_or_404(
            self.queryset, pk=pk, patient__pk=patient_pk
        )
        study.is_active = False
        study.save()
        return Response({"id": pk}, status=status.HTTP_200_OK)
