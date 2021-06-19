from typing import Dict

from rest_framework.serializers import (
    BooleanField,
    CharField,
    DateField,
    EmailField,
    IntegerField,
    Serializer,
)
from rest_framework.validators import UniqueValidator

from api.models import PatientModel


class PatientSerializer(Serializer):
    """
    Patient Serializer
    Helps to validate the incoming request data and convert the object model to JSON object as output
    """

    class Meta:
        model = PatientModel

    id = IntegerField(read_only=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    birth_date = DateField(required=False)
    email = EmailField(
        max_length=50, validators=[UniqueValidator(queryset=PatientModel.objects.all())]
    )
    is_active = BooleanField()

    def create(self, validated_data):
        return PatientModel.objects.create(**validated_data)

    def update(self, instance: PatientModel, validated_data: Dict):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.birth_date = validated_data.get("birth_date")
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance
