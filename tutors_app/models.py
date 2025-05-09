from django.db import models

# Create your models here.
class Tutor(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)

    def __str__(self):
        return self.name