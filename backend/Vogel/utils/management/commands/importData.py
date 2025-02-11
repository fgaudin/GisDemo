import os
import json
import arrow
from django.core.management.base import BaseCommand

from observation.models import Observation
from species.models import Species
from django.contrib.gis.geos import Point
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = "import JSON data"

    def readFilesInDirectory(self, directory):
        files = []
        for file in os.listdir(directory):
            if file.endswith(".json"):
                files.append(file)
        return files

    def importData(self, directory):
        species = {}
        observations = []

        files = self.readFilesInDirectory(directory)
        self.stdout.write(
            f"Found {files[0] if len(files) else '0 files'} in {directory}"
        )

        for file in files:
            with open(directory + "/" + file, "r") as f:
                data = json.load(f)
                for item in data["data"]:
                    species[item["species_array"]["id"]] = item["species_array"]

                    # extract date from html span element
                    soup = BeautifulSoup(item["date"], "html.parser")
                    d = arrow.get(soup.get_text(), "DD MMM YYYY").to("UTC").datetime
                    obs = {
                        "location": Point(float(item["lon"]), float(item["lat"])),
                        "count": int(
                            "".join(filter(str.isdigit, item["birds_count"])) or 0
                        ),
                        "date": d,
                        "species_id": item["species_array"]["id"],
                    }
                    observations.append(obs)

        for id, sp in species.items():
            defaults = {
                "name": sp["name"],
                "plural": sp["name_plur"],
                "latin_name": sp["latin_name"],
                "category": sp["category"],
                "rarity": sp["rarity"],
            }
            obj, created = Species.objects.get_or_create(
                defaults, latin_name=sp["latin_name"]
            )
            species[id] = obj

        Observation.objects.filter(imported=True).delete()

        for o in observations:
            o["species_id"] = species[o["species_id"]].id
            Observation.objects.create(**o)

    def add_arguments(self, parser):
        parser.add_argument("directory", nargs="?", type=str)

    def handle(self, *args, **options):
        self.importData(options["directory"])
