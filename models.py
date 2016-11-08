from django.db import models
from django.conf import settings

class SiteSetting(models.Model):
    organization = models.CharField(max_length=75)
    description = models.CharField(max_length=512, null=True)
    background = models.ImageField(upload_to='background', null=True,
                                   blank=True)

class SidebarLink(models.Model):
    url = models.CharField(max_length=75)
    name = models.CharField(max_length=75)
    settings = models.ForeignKey(SiteSetting, on_delete=models.CASCADE)

# These will not be available on Mobile
class TitlebarLink(models.Model):
    url = models.CharField(max_length=75)
    name = models.CharField(max_length=75)
    settings = models.ForeignKey(SiteSetting, on_delete=models.CASCADE)
