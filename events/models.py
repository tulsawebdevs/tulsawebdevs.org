from hashlib import md5

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils.translation import ugettext_lazy as _
from django_pgjson.fields import JsonField

from utils.geo import geocode


class Location(models.Model):
    """Geo and meta representation of the location an event can occur"""

    name = models.CharField(_('Location Name'), max_length=255)
    address = models.CharField(_('Address'), max_length=255, blank=True, null=True, unique=True)
    location = models.PointField(_('Location'), blank=True, null=True)
    location_hash = models.CharField(max_length=32, null=True)
    meta = JsonField(_('metadata'), blank=True, null=True)

    objects = models.GeoManager()

    def __str__(self):
        return "{name}".format(name=self.name)

    def save(self, **kwargs):
        location_hash = md5(
            '{}@{}'.format(self.name, self.address).encode('utf-8'))
        if self.location_hash != location_hash and self.address:
            self.meta = geocode(self.address).raw
            pos = [float(coord) for coord in [self.meta.get('lon'), self.meta.get('lat')]]
            self.location = Point(*pos)
            self.location_hash = location_hash
        super(Location, self).save(**kwargs)
