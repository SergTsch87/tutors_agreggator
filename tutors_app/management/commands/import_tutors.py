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

    def handle(self, *args, **options):
        path = options['path']

        if not os.path.exists(path):
            self.stderr.write(self.style.ERROR(f"File not found: {path}"))
            return
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        created_count = 0
        for entry in data:
            obj, created = Tutor.objects.get_or_create(
                name=entry['name'],
                defaults={'subject': entry['subject']}
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {created_count} new tutors."))
        # return super().handle(*args, **options)