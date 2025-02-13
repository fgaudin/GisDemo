import datetime
from django.test import TestCase
from ninja.testing import TestClient

from .models import Species
from species.api import router


class SpeciesApiTest(TestCase):
    def setUp(self):
        self.maxDiff = None

        self.client = TestClient(router)

        self.eagle = Species.objects.create(
            name="Eagle",
            plural="Eagles",
            latin_name="Accipitridae",
            category="A",
            rarity="common",
            avatar_url="image.jpg",
        )
        self.sparrow = Species.objects.create(
            name="House sparrow",
            plural="House sparrows",
            latin_name="Passer domesticus",
            category="A",
            rarity="common",
            avatar_url="image2.jpg",
        )

    def test_get(self):

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200, response.content)

        data = response.json()

        expected = [
            {
                "id": self.eagle.id,
                "name": "Eagle",
                "plural": "Eagles",
                "latin_name": "Accipitridae",
                "category": "A",
                "rarity": "common",
                "avatar_url": "image.jpg",
            },
            {
                "id": self.sparrow.id,
                "name": "House sparrow",
                "plural": "House sparrows",
                "latin_name": "Passer domesticus",
                "category": "A",
                "rarity": "common",
                "avatar_url": "image2.jpg",
            },
        ]

        self.assertEqual(data, expected)
