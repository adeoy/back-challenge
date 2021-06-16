from django.db import models


class Patient(models.Model):
    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    birth_date = models.DateField(null=True)
    email = models.EmailField(null=True)
    national_id = models.TextField(null=True)

    class Meta:
        db_table = "patient"
