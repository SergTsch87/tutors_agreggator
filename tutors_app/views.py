# from django.shortcuts import render

# Create your views here.

# with templates
# Class-Based View (CBV):
from django.views.generic import ListView
from .models import Tutor


class TutorListView(ListView):
    model = Tutor
    template_name = 'tutors_app/tutors_list.html'
    context_object_name = 'tutors'
