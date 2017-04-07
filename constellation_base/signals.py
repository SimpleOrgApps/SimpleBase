from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from .models import LocalGroupACL


@receiver(user_logged_in)
def addSupplementalGroups(sender, user, request, **kwargs):
    """Apply additional groups on login"""
    for group in list(LocalGroupACL.objects.all()):
        supGroup = group.group
        if user.username in group.members:
            supGroup.user_set.add(user)
        else:
            supGroup.user_set.remove(user)
