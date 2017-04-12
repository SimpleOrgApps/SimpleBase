from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from .models import LocalGroupACLEntry


@receiver(user_logged_in)
def addSupplementalGroups(sender, user, request, **kwargs):
    """Apply additional groups on login"""
    supGroups = LocalGroupACLEntry.objects.filter(username=user.username)

    for group in supGroups:
        group.group.user_set.add(user)
