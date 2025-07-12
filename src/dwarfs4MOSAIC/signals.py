"""
Signal handlers for synchronizing Django User and custom model Tbl_researcher.

This module listens to creation or update events on User model to:
- Update related Tbl_researcher fields when a User is updated.
"""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Tbl_researcher

# Update linked Tbl_researcher fields when a User instance is saved.
# Synchronizes the name and email of Tbl_researcher with the corresponding User
# first_name, last_name, and email fields.
# If no Tbl_researcher is linked to the User, silently do nothing.
@receiver(post_save, sender=User)
def update_researcher(sender, instance, **kwargs):
    try:
        researcher = instance.researcher
        researcher.name = f"{instance.first_name} {instance.last_name}".strip()
        researcher.email = instance.email
        researcher.save()
    except Tbl_researcher.DoesNotExist:
        pass  # No linked researcher found; do nothing
