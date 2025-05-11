# from django.shortcuts import render

# Create your views here.

# with templates
# Class-Based View (CBV):
from django.views.generic import ListView, DetailView
from .models import Tutor


class TutorListView(ListView):
    model = Tutor
    template_name = 'tutors_app/tutors_list.html'
    context_object_name = 'tutors'

    # filter queryset if a subject is passed
    def get_queryset(self):
        queryset = super().get_queryset()
        subject = self.request.GET.get("subject")  # to read the filter value
        if subject:
            queryset = queryset.filter(subject__iexact=subject)
        return queryset


class TutorDetailView(DetailView):
    model = Tutor
    template_name = 'tutors_app/tutors_detail.html'
    context_object_name = 'tutor'