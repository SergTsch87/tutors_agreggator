from django.contrib import admin
from .models import Tutor, Subject

# Register your models here.
# admin.site.register(Tutor)

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    search_fields = ('name', 'subject')
    list_filter = ('subject',)


admin.site.register(Subject)