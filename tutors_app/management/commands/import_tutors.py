import json
import os
from django.core.management.base import BaseCommand
from tutors_app.models import Tutor, Subject
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

        parser.add_argument(
            '--limit',
            type=int,
            help='Limit the number of tutors to import'
        )

    # is the entry point for your command
    def handle(self, *args, **options):
        path = options['path']  # accesses the value passed from the command line (e.g. --path=data/tutors.json)
        limit = options.get('limit')  # to import only a limited number of tutors

        if not os.path.exists(path):
            # self.stderr.write - Print styled error messages
            self.stderr.write(self.style.ERROR(f"❌ File not found: {path}"))
            return
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if limit is not None:
            data = data[:limit]

        created_count = 0
        for entry in data:
            # get_or_create - Avoid creating duplicates
            subj_name = entry['subject'].strip()
            # Either get existing Subject or create a new one
            subj_obj, _ = Subject.objects.get_or_create(name=subj_name)


            # Var 2)
            # # Now create the Tutor with ForeignKey to Subject
            # Tutor.objects.create(name=entry['name'], subject=subj_obj)
            # To avoid data duplication or bad links from pre-migration data
            # Tutor.objects.all().delete()
            # Subject.objects.all().delete()


            obj, created = Tutor.objects.get_or_create(
                name=entry['name'],
                # defaults={'subject': entry['subject']}
                subject=subj_obj
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Created {entry['name']}"))  # ✅ Green (successful operation)
            else:
                self.stdout.write(self.style.WARNING(f"⚠️  Skipped (already exists): {entry['name']}"))   # ⚠️ Yellow (non-critical info)

        self.stdout.write(self.style.SUCCESS(f"Imported {created_count} new tutors."))
        # self.style.SUCCESS - Print colored success message
        
        # self.style.ERROR('text') — ❌ Red (critical failure)