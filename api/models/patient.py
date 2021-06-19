from django.db import models


class PatientModel(models.Model):
    """
    Patient Model
    Fields: id, first_name, last_name, birth_date, email
    """

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "patient"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
