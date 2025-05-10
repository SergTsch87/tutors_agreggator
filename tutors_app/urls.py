# with templates
# # Class-Based View (CBV):
# from tutors_app.views import HomeView
from django.urls import path
from .views import TutorListView, TutorDetailView


app_name = 'tutors'

urlpatterns = [
    path('', TutorListView.as_view(), name='tutors_list'),
    path('<int:pk>/', TutorDetailView.as_view(), name='tutor_detail'),
]