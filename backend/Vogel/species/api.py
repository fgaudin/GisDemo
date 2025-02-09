import decimal
from typing import List
from ninja import ModelSchema, Router

from .models import Species

router = Router()


class SpeciesOut(ModelSchema):

    class Meta:
        model = Species
        fields = ['id', 'name', 'plural', 'latin_name', 'category', 'rarity']
                  

@router.get("/", response=List[SpeciesOut])
def list_species(request):
    qs = Species.objects.all()
    return qs