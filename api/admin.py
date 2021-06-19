from django.contrib import admin

from api import models

# Register your models here.

admin.site.register(models.PatientModel)
admin.site.register(models.StudyModel)
