from django.db import models
from django.utils.translation import gettext as _

class Airport(models.Model):
    iata = models.CharField(_("IATA"), max_length=3, unique=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.iata} ({self.city}, {self.state})"
    
