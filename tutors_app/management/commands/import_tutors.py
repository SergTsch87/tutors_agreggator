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

    # is the entry point for your command
    def handle(self, *args, **options):
        path = options['path']  # accesses the value passed from the command line (e.g. --path=data/tutors.json)

        if not os.path.exists(path):
            # self.stderr.write - Print styled error messages
            self.stderr.write(self.style.ERROR(f"File not found: {path}"))
            return
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        created_count = 0
        for entry in data:
            # get_or_create - Avoid creating duplicates
            obj, created = Tutor.objects.get_or_create(
                name=entry['name'],
                defaults={'subject': entry['subject']}
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {created_count} new tutors."))
        # self.style.SUCCESS - Print colored success message
        # return super().handle(*args, **options)