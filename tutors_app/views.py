from django.shortcuts import render

# Create your views here.

# with templates
# Class-Based View (CBV):
from django.views.generic import TemplateView


class HomeView(TemplateView):
    # template_name = 'G:\Windows\Meni\Work\Python\Lessons Python\tutor_dj_scrap\tutors_app\templates\tutors_app\base.html'
    template_name = 'tutors_app/base.html'
