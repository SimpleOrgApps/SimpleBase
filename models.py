from django.db import models

class SiteSetting(models.Model):
    organization = models.CharField(max_length=75)
    description = models.CharField(max_length=512, null=True)
    background = models.ImageField(upload_to='SimpleBase/static/SimpleBase/background', null=True,
                                   blank=True)

    def __str__(self):
        return self.organization
