from django.contrib.gis.db import models
from django.utils.translation import gettext as _

from species.models import Species


class Observation(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    date = models.DateTimeField(_("Date"))
    count = models.IntegerField(_("Count"))
    location = models.PointField(_("Location"))

    def __str__(self):
        return f"{self.species.name} - {self.date}"