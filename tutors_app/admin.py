from django.contrib import admin
from .models import Tutor, Subject
# from .admin import TutorAdmin

# Register your models here.
@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # removed 'subject' because M2M is not allowed here
    # search_fields = ('name', 'subject__name')
    list_filter = ['subjects']  # ✅ M2M fields allowed here
    # raw_id_fields = ('subjects',)  #  is not for M2M
    filter_horizontal = ['subjects']  # cleaner UI for many-to-many / # ✅ adds a better UI for M2M selection


# admin.site.register(Subject)
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


# admin.site.register(Tutor, TutorAdmin)
# admin.site.register(Subject)