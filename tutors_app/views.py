# with templates
# Class-Based View (CBV):
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from django.db.models import Q  # Q-objects for complex queries
from django.core.paginator import Paginator
from .models import Tutor, Subject
# from django.shortcuts import render
from django.db.models.functions import Lower


class TutorListView(ListView):
    model = Tutor
    template_name = 'tutors_app/tutors_list.html'
    context_object_name = 'tutors'
    paginate_by = 10  # ✅ NEW: This enables automatic pagination

    # Modify get_queryset() to include q from GET
    # filter queryset if a subject is passed
    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('subjects')  # ✅ Use prefetch_related for M2M
        
        # Gets the value of the GET parameter ?subject=25
        # ✅ NEW: Get subject and search query
        subject_id = self.request.GET.get("subject")  # to read the filter value
        search_query = self.request.GET.get("q", "").strip()

        # Allow filtering by tutor name substring AND subject at the same time
        if subject_id:
            # Filters tutors by subject ID (foreign key comparison)
            queryset = queryset.filter(subjects__id=subject_id)
            # or...
            # queryset = queryset.filter(subjects__name__iexact=subject_id)
        # if name:
        #     # Filters tutors by name
        #     queryset = queryset.filter(name__icontains=name)

        # ✅ Filter by name or subject match (case-insensitive)
        if search_query:
            # # ! Use the simple version if you're only implementing name-based search for now
            # queryset = queryset.filter(name__icontains=search_query)

            # # Optional: filter using full_name in Python (slower, but works for demo)
            # queryset = [tutor for tutor in queryset if search_query.lower() in tutor.name.lower()]

            queryset = queryset.annotate(
                lower_name=Lower("name")
            ).filter(
                    lower_name__icontains=search_query.lower()
                )

        return queryset
    
    # Pass the list of subjects to the template
    def get_context_data(self, **kwargs):
        # Gets default context from ListView (which includes 'tutors')
        context = super().get_context_data(**kwargs)

        # # Get all distinct subjects associated with tutors, including subject objects
        # subject_ids = Tutor.objects.values_list('subject', flat=True).distinct()
        # ✅ Fetch all subjects to show in filter dropdown
        context["subjects"] = Subject.objects.all()

        # Adds a list of unique subject IDs (used in dropdown or filter list)
        # context["subjects"] = Tutor.objects.values_list("subject", flat=True).distinct()

        # # ✅ Pass the selected subject ID for keeping the filter state
        # # to show the currently selected subject at the top of the page
        # subject_id = self.request.GET.get("subject")
        # if subject_id:
        #     context['selected_subject'] = Subject.objects.filter(id=subject_id).first()

        # ✅ Return current filters to template for display
        context["selected_subject"] = self.request.GET.get("subject", "")
        context["search_query"] = self.request.GET.get("q", "").strip()

        return context


class TutorDetailView(DetailView):
    model = Tutor
    template_name = 'tutors_app/tutor_detail.html'
    context_object_name = 'tutor'