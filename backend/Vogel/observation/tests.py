import datetime
from django.test import TestCase
from ninja.testing import TestClient

from observation.models import Observation
from species.models import Species
from observation.api import router


class ObservationApiTest(TestCase):
    def setUp(self):
        self.maxDiff = None

        self.client = TestClient(router)

        eagle = Species.objects.create(
            name="Eagle",
            plural="Eagles",
            latin_name="Accipitridae",
            category="A",
            rarity="common",
            avatar_url="image.jpg",
        )
        sparrow = Species.objects.create(
            name="House sparrow",
            plural="House sparrows",
            latin_name="Passer domesticus",
            category="A",
            rarity="common",
            avatar_url="image2.jpg",
        )

        Observation.objects.create(
            species=sparrow,
            date="2021-01-01",
            count=2,
            location="POINT (12.492373 41.890210)",
        )
        Observation.objects.create(
            species=eagle,
            date="2021-01-02",
            count=5,
            location="POINT (14.492373 43.890210)",
        )

    def test_get(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("count"), 2)
        expected = [
            {
                "id": 2,
                "count": 5,
                "date": "2021-01-02",
                "latitude": "43.89021",
                "longitude": "14.492373",
                "species": {
                    "id": 1,
                    "name": "Eagle",
                    "plural": "Eagles",
                    "latin_name": "Accipitridae",
                    "category": "A",
                    "rarity": "common",
                    "avatar_url": "image.jpg",
                },
            },
            {
                "id": 1,
                "count": 2,
                "date": "2021-01-01",
                "latitude": "41.89021",
                "longitude": "12.492373",
                "species": {
                    "id": 2,
                    "name": "House sparrow",
                    "plural": "House sparrows",
                    "latin_name": "Passer domesticus",
                    "category": "A",
                    "rarity": "common",
                    "avatar_url": "image2.jpg",
                },
            },
        ]
        self.assertEqual(data.get("items"), expected)

    def test_get_filtered(self):
        response = self.client.post(
            "/filtered/",
            json={"region": [[10, 42], [20, 42], [20, 44], [10, 44], [10, 42]]},
        )

        self.assertEqual(response.status_code, 200, response.content)
        data = response.json()
        self.assertEqual(data.get("count"), 1)
        self.assertEqual(data.get("items")[0]["species"]["name"], "Eagle")

    def test_get_add_observation(self):
        sparrow = Species.objects.get(name="House sparrow")

        response = self.client.post(
            "/",
            json={
                "count": 3,
                "date": "2021-01-03",
                "species_id": sparrow.id,
                "latitude": 44.89021,
                "longitude": 15.492373,
            },
        )
        self.assertEqual(response.status_code, 201, response.content)

        data = response.json()
        observation = Observation.objects.get(id=data["id"])
        self.assertEqual(observation.count, 3)
        self.assertEqual(observation.date, datetime.date(2021, 1, 3))
        self.assertEqual(observation.species, sparrow)
        self.assertEqual(observation.location.x, 15.492373)
        self.assertEqual(observation.location.y, 44.89021)
