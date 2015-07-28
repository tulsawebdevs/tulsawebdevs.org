from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Location(models.Model):
    """Geo and meta representation of the location an event can occur"""

    name = models.CharField(_('Location Name'), max_length=255)
    address = models.CharField(_('Address'), max_length=255, blank=True, null=True, unique=True)
    location = models.PointField(_('Location'), blank=True, null=True)

    objects = models.GeoManager()

    def __str__(self):
        return "{name}".format(name=self.name)
