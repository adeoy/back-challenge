from typing import Dict

from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    BooleanField,
    CharField,
    ChoiceField,
    IntegerField,
    Serializer,
)

from api.constants import STUDY_TYPES, URGENCY_LEVELS
from api.models import PatientModel, StudyModel


class StudySerializer(Serializer):
    """
    Patient Serializer
    Helps to validate the incoming request data and convert the object model to JSON object as output
    """

    class Meta:
        model = StudyModel

    id = IntegerField(read_only=True)
    urgency_level = ChoiceField(choices=URGENCY_LEVELS)
    body_part = CharField(max_length=50)
    description = CharField(max_length=100)
    type = ChoiceField(choices=STUDY_TYPES)
    is_active = BooleanField()

    def create(self, validated_data):
        patient: PatientModel = get_object_or_404(
            PatientModel.objects.all(), pk=validated_data.get("patient_id")
        )
        return StudyModel.objects.create(patient=patient, **validated_data)

    def update(self, instance: StudyModel, validated_data: Dict):
        instance.urgency_level = validated_data.get(
            "urgency_level", instance.urgency_level
        )
        instance.body_part = validated_data.get("body_part", instance.body_part)
        instance.description = validated_data.get("description", instance.description)
        instance.type = validated_data.get("type", instance.type)
        instance.patient = get_object_or_404(
            PatientModel.objects.all(),
            pk=validated_data.get("patient_id", instance.patient.id),
        )
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance
