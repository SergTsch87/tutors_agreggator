from django.db import models
from django.urls import reverse

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)  # The unique=True ensures no duplicate subjects.

    def __str__(self):
        return self.name


class TutorManager(models.Manager):
    def by_subject(self, subject_name):
        return self.select_related('subject').filter(subject__name=subject_name)
    

class Tutor(models.Model):
    name = models.CharField(max_length=100)
    # subject = models.CharField(max_length=100)  # ← This will be changed
    # subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tutors')  # creates a many-to-one link from Tutor to Subject
    subject = models.ManyToManyField(Subject, related_name='tutors')  # creates a many-to-many link between Tutor and Subject

    objects = TutorManager()

    def __str__(self):
        return self.name

    def formatted_subject(self):
        return self.subject.name.title()
    
    def get_absolute_url(self):
        return reverse('tutors:tutor_detail', args=[str(self.pk)])