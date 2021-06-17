from django.db import models


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = "patient"


class Study(models.Model):
    id = models.AutoField(primary_key=True)
    urgency_level = models.CharField(max_length=50)
    body_part = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    class Meta:
        db_table = "study"
