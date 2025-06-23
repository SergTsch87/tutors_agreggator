from django.core.management.base import BaseCommand
from tutors_app.models import Tutor, Subject
from sandbox_parse import get_html, parse_tutors_page_buki

class Command(BaseCommand):
    help = 'Scrapes tutors from Buki and saves them into the DB'

    def handle(self, *args, **kwargs):
        num_page = 5
        url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/"
        html = get_html(url)
        tutors_data = parse_tutors_page_buki(html)

        for item in tutors_data:
            id_tutor = item.get("id_tutor")
            name = item.get("name", "").strip()
            price = item.get("price", 0)
            rating = item.get("rating", None)
            number_of_reviews = item.get("number_of_reviews", None)
            education = item.get("education", "").strip()
            experience = item.get("experience", "").strip()
            about_myself = item.get("about_myself", "") # .strip()
            city_or_online = item.get("city_or_online", "") # .strip()
            subject_names = item.get("objects", [])

            # if not name:
            #     continue
            if not id_tutor:
                continue

            # tutor, created = Tutor.objects.get_or_create(name=name, defaults={
            tutor, created = Tutor.objects.get_or_create(id_tutor=id_tutor, defaults={
                "name": name, # new
                "price": price,
                "rating": rating,
                "number_of_reviews": number_of_reviews,
                "education": education,
                "experience": experience,
                "about_myself": about_myself,
                "city_or_online": city_or_online
            })

            if not created:
                self.stdout.write(f"Skipped existing tutor: {name}")
                continue

            for subject_name in subject_names:
                subject, _ = Subject.objects.get_or_create(name=subject_name.strip())
                tutor.subjects.add(subject)

            tutor.save()
            self.stdout.write(f"Saved tutor: {name}")