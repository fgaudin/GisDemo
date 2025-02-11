import requests
import environ
import time
from django.core.management.base import BaseCommand

from species.models import Species


class Command(BaseCommand):
    help = "search images"

    def searchImages(self):
        env = environ.Env()
        url = env.str("BIRD_API")
        base_img_url = env.str("BIRD_IMAGE_BASE")

        species = Species.objects.all()
        for sp in species:
            actual_url = f"{url}{sp.name.replace('|', '')}"
            print(actual_url)
            response = requests.get(actual_url)
            if response.status_code == 200:
                data = response.json()
                sp.avatar_url = f"{base_img_url}{data['folder']}{data['img']}"
                sp.save()

            time.sleep(0.5)

    def handle(self, *args, **options):
        self.searchImages()
