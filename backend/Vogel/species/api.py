import decimal
from typing import List
from ninja import ModelSchema, Router

from .models import Species

router = Router()


class SpeciesOut(ModelSchema):

    class Meta:
        model = Species
        fields = [
            "id",
            "name",
            "plural",
            "latin_name",
            "category",
            "rarity",
            "avatar_url",
        ]

    @staticmethod
    def resolve_name(obj):
        return obj.name.replace("|", "")


@router.get("/", response=List[SpeciesOut])
def list_species(request):
    qs = Species.objects.all().order_by("name", "id")
    return qs
