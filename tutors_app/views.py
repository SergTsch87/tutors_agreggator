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
        queryset = super().get_queryset().select_related('subject')
        subject = self.request.GET.get("subject")  # to read the filter value
        if subject:
            # to filter by id:
            queryset = queryset.filter(subject__id=subject)
            
            # # to filter by name: not work...
            # queryset = queryset.filter(subject__name__iexact=subject)

            # queryset = queryset.filter(subject__iexact=subject)
        return queryset
    
    # Pass the list of subjects to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subjects"] = Tutor.objects.values_list("subject", flat=True).distinct()
        return context


class TutorDetailView(DetailView):
    model = Tutor
    template_name = 'tutors_app/tutor_detail.html'
    context_object_name = 'tutor'