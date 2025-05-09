# with templates
# # Class-Based View (CBV):
# from tutors_app.views import HomeView
from django.urls import path
from .views import TutorListView


urlpatterns = [
    path('', TutorListView.as_view(), name='tutor_list'),
]