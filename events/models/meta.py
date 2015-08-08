# -*- coding: utf-8 -*-
from hashlib import md5

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django_pgjson.fields import JsonField

from utils.geo import geocode


class Location(models.Model):
    """Geo and meta representation of a location"""

    name = models.CharField(
        _('Location Name'),
        max_length=255
    )

    address = models.CharField(
        _('Address'),
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )

    location = models.PointField(
        _('Location'),
        blank=True,
        null=True
    )

    location_hash = models.CharField(
        max_length=32,
        null=True
    )

    meta = JsonField(
        _('metadata'),
        blank=True,
        null=True
    )

    objects = models.GeoManager()

    def __str__(self):
        return "{name}".format(name=self.name)

    def save(self, **kwargs):
        location_hash = md5(
            '{}@{}'.format(self.name, self.address).encode('utf-8')).hexdigest()
        if self.location_hash != location_hash and self.address:
            location_geocode = geocode(self.address)
            if location_geocode:
                self.meta = location_geocode.raw
                pos = [float(self.meta.get(coord)) for coord in ['lon', 'lat']]
                self.location = Point(*pos)
                self.location_hash = location_hash
            else:
                self.meta = {"geocoded": False}
                self.location = None
        super().save(**kwargs)
