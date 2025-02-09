import decimal
from typing import List
from ninja import ModelSchema, Schema, Router

from species.api import SpeciesOut

from .models import Observation

router = Router()


class ObservationOut(ModelSchema):
    lattitude: decimal.Decimal
    longitude: decimal.Decimal
    species: SpeciesOut

    class Meta:
        model = Observation
        fields = ['id', 'count', 'date']
                  
    @staticmethod
    def resolve_lattitude(obj):
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