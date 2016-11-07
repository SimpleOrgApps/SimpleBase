from django.db import models
from django.conf import settings

class SiteSetting(models.Model):
    organization = models.CharField(max_length=75)
    description = models.CharField(max_length=512, null=True)
    background = models.ImageField(upload_to='background', null=True,
                                   blank=True)

    def __str__(self):
        return self.organization
