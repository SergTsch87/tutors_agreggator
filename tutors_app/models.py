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
    id_tutor = models.IntegerField(unique=True, null=True, blank=True) # after migration and cleanup, you can later remove `null=True`
    # you can later remove null=True and blank=True, once you're sure all records have proper id_tutor values
    
    name = models.CharField(max_length=100)

# --------------------
# Fields that are used in the `defaults` of `get_or_create` (defaults)

    price = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    number_of_reviews = models.IntegerField(blank=True, null=True)
    
    # In Django forms, it renders as an HTML <textarea> element:
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    about_myself = models.TextField(blank=True, null=True)
    
    city = models.CharField(max_length=100, blank=True, null=True)
    is_online = models.BooleanField(default=False)
    # Filter easily (.filter(is_online=True)) or group by city

    # city_or_online = models.CharField(max_length=100, blank=True, null=True, default='online')
    # set default='online' for city_or_online in Tutor
# --------------------

    # subject = models.CharField(max_length=100)  # ← This will be changed
    # subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tutors')  # creates a many-to-one link from Tutor to Subject
    subjects = models.ManyToManyField(Subject, related_name='tutors')  # creates a many-to-many link between Tutor and Subject

    objects = TutorManager()

    def __str__(self):
        return self.name
        # return self.name + ' ' + self.name #  update ???

    def formatted_subject(self):
        return self.subjects.name.title()
    
    def get_absolute_url(self):
        return reverse('tutors:tutor_detail', args=[str(self.pk)])

    @property
    def first_name(self):
        return self.name.split()[0] if self.name else ""

    @property
    def last_name(self):
        parts = self.name.split() 
        return parts[-1] if len(parts) > 1 else ""