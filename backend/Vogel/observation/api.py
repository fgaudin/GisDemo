import decimal
from typing import List
from ninja import ModelSchema, Schema
from ninja.pagination import RouterPaginated
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import Polygon

from species.api import SpeciesOut

from .models import Observation

LIMIT = 200

router = RouterPaginated()


class ObservationIn(ModelSchema):
    latitude: decimal.Decimal
    longitude: decimal.Decimal

    class Meta:
        model = Observation
        fields = ["count", "date", "species"]


class ObservationIdOut(ModelSchema):

    class Meta:
        model = Observation
        fields = ["id"]


class ObservationOut(ModelSchema):
    latitude: decimal.Decimal
    longitude: decimal.Decimal
    species: SpeciesOut

    class Meta:
        model = Observation
        fields = ["id", "count", "date"]

    @staticmethod
    def resolve_latitude(obj):
        if not obj.location:
            return
        return obj.location.y

    @staticmethod
    def resolve_longitude(obj):
        if not obj.location:
            return
        return obj.location.x


class RegionFilterIn(Schema):
    region: List[List[decimal.Decimal]]


@router.get("/", response=List[ObservationOut])
def list_observations(request):
    qs = Observation.objects.all().order_by("-date", "id")[:LIMIT]
    return qs


@router.post("/filtered/", response=List[ObservationOut])
def filter_observations(request, payload: RegionFilterIn):
    poly = Polygon(payload.region)
    qs = Observation.objects.filter(location__intersects=poly).order_by("-date", "id")[
        :LIMIT
    ]
    return qs


@router.post("/", response={201: ObservationIdOut})
def add_observation(request, payload: ObservationIn):
    observation = Observation()
    observation.count = payload.count
    observation.date = payload.date
    observation.species_id = payload.species
    observation.location = Point(float(payload.longitude), float(payload.latitude))
    observation.save()

    return 201, {"id": observation.id}
