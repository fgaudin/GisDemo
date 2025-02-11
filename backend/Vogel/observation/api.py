import decimal
from typing import List
from ninja import ModelSchema, Schema, Router
from django.contrib.gis.geos import Point

from species.api import SpeciesOut

from .models import Observation

router = Router()

class ObservationIn(ModelSchema):
    latitude: decimal.Decimal
    longitude: decimal.Decimal

    class Meta:
        model = Observation
        fields = ['count', 'date', 'species']


class ObservationOut(ModelSchema):
    latitude: decimal.Decimal
    longitude: decimal.Decimal
    species: SpeciesOut

    class Meta:
        model = Observation
        fields = ['id', 'count', 'date']
                  
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


@router.get("/", response=List[ObservationOut])
def list_observations(request):
    qs = Observation.objects.all()
    return qs

@router.post("/")
def add_observation(request, payload: ObservationIn):
    observation = Observation()
    observation.count = payload.count
    observation.date = payload.date
    observation.species_id = payload.species
    observation.location = Point(float(payload.longitude), float(payload.latitude))
    observation.save()

    return {"id": observation.id}