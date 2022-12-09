from django.db import models

# Create your models here.
class FormModel(models.Model):
    csv_file = models.FileField()

    def register(self):
        self.save()
