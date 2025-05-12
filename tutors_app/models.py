from django.db import models
from django.urls import reverse

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Tutor(models.Model):
    name = models.CharField(max_length=100)
    # subject = models.CharField(max_length=100)  # ← This will be changed
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='titors')

    def __str__(self):
        return self.name

    def formatted_subject(self):
        return self.subject.title()
    
    def get_absolute_url(self):
        return reverse('tutors:tutor_detail', args=[str(self.pk)])