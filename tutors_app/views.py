from django.shortcuts import render

# Create your views here.

# with templates
# Class-Based View (CBV):
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'tutors_app/base.html'
