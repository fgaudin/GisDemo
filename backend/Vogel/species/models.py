from django.db import models
from django.utils.translation import gettext as _


class Species(models.Model):
    name = models.CharField(_("Name"), max_length=150, unique=True)
    plural = models.CharField(_("Plural name"), max_length=150)
    latin_name = models.CharField(_("Latin name"), max_length=150, unique=True)
    category = models.CharField(_("Category"), max_length=3)
    rarity = models.CharField(_("Rarity"), max_length=15)
    avatar_url = models.URLField(_("Avatar URL"), null=True, blank=True)

    def __str__(self):
        return self.name
