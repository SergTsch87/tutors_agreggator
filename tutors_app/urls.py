
# with templates
# # Class-Based View (CBV):
# from tutors_app.views import HomeView
from django.urls import path
from .views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
