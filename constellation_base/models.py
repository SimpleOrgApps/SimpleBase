from django.db import models
from django.contrib.auth.models import Group


class SiteSetting(models.Model):
    organization = models.CharField(max_length=75)
    description = models.CharField(max_length=512, null=True)
    background = models.ImageField(upload_to='background', null=True,
                                   blank=True)


# These will not be available on Mobile
class TitlebarLink(models.Model):
    url = models.CharField(max_length=75)
    name = models.CharField(max_length=75)
    settings = models.ForeignKey(SiteSetting, on_delete=models.CASCADE)


class GlobalTemplateSettings():
    def __init__(self, allowBackground):
        self.allowBackground = allowBackground
        self.background = None
        try:
            site_settings = SiteSetting.objects.get(pk=1)
            self.organization = site_settings.organization
            self.description = site_settings.description
            self.background = site_settings.background if self.allowBackground else None
        except SiteSetting.DoesNotExist:
            self.organization = "My Organization"
            self.description = "An organization description will need to be set up in \
            the admin panel"

        try:
            self.titlebar_links = TitlebarLink.objects.all()
        except TitlebarLink.DoesNotExist:
            self.titlebar_links = None

    def settings_dict(self):
        return {
            'background': self.background,
            'description': self.description,
            'organization': self.organization,
            'titlebar_links': self.titlebar_links,
        }


class LocalGroupACL(models.Model):
    """ACL for Local Groups that don't exist in other authentication sources"""
    group = models.ForeignKey(Group)

    # This contains a delimited string of usernames that are members of this
    # group.  The delimiter is not important because the check is just done
    # with a 'user in groupACL.members' style check.
    members = models.TextField()

    def __str__(self):
        return "Supplemental Group: {0}".format(self.group)

    class Meta:
        verbose_name = "Supplemental Group ACL"
        verbose_name_plural = "Supplemental Group ACLs"
