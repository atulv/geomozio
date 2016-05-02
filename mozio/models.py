from django.contrib.gis.db import models
from geojson import Polygon

class Provider(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=12, db_index=True)
    language = models.CharField(max_length=4)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'language': self.language,
            'currency': self.currency
        }

class ServiceArea(models.Model):
    provider = models.ForeignKey(Provider)
    name = models.CharField(max_length=255, db_index=True)
    price = models.FloatField()
    region = models.PolygonField()
    objects = models.GeoManager()
    
    class Meta:
        unique_together = ('provider', 'name')

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'provider': self.provider_id,
            'name': self.name,
            'price': self.price,
            'geojson': Polygon(self.region.coords)
        }
