from django.db import models

from api.models.patient import PatientModel


class StudyModel(models.Model):
    """
    Study Model
    Fields: id, urgency_level, body_part, description, type, patient
    """

    id = models.AutoField(primary_key=True)
    urgency_level = models.CharField(max_length=4)
    body_part = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    patient = models.ForeignKey(
        PatientModel,
        on_delete=models.CASCADE,
        related_name="studies",
        related_query_name="study",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "study"

    def __str__(self):
        return f"{self.urgency_level} - {self.body_part} - {self.type}"
