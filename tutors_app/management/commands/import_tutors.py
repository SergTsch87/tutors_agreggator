import json
import os
from django.core.management.base import BaseCommand
from tutors_app.models import Tutor
from django.conf import settings


class Command(BaseCommand):
    help = "Import tutors from a JSON file"
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='Path to the JSON file with tutor data',
            default=os.path.join(settings.BASE_DIR, 'tutors_data.json')
        )