from django.contrib import admin
from .models import Tutor, Subject

# Register your models here.
@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'subjects')
    # search_fields = ('name', 'subject__name')
    list_filter = ('subjects',)
    raw_id_fields = ('subjects',)
    filter_horizontal = ('subjects',)  # cleaner UI for many-to-many


# admin.site.register(Subject)
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


# admin.site.register(Tutor, TutorAdmin)
# admin.site.register(Subject)