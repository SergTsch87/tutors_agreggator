from django.db import models
from django.urls import reverse

# Create your models here.
class Tutor(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def formatted_subject(self):
        return self.subject.title()
    
    def get_absolute_url(self):
        return reverse('tutors:tutor_detail', args=[str(self.pk)])