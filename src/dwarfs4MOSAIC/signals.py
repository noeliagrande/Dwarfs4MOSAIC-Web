"""
Signal handlers for synchronizing Django User and custom model Tbl_researcher.

This module listens to creation or update events on User model to:
- Update related Tbl_researcher fields when a User is updated.
"""

from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Tbl_researcher


# Signal handler to create a Tbl_researcher instance
# automatically whenever a new User is created,
# except if the User is a superuser.
@receiver(post_save, sender=User)
def create_researcher_for_new_user(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        # Create the related Tbl_researcher linked to this User
        Tbl_researcher.objects.create(
            user=instance,
            name=f"{instance.first_name} {instance.last_name}".strip(),
            email=instance.email,
        )


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

# When a Researcher is deleted, also delete the linked User.
@receiver(post_delete, sender=Tbl_researcher)
def delete_user_with_researcher(sender, instance, **kwargs):
    user = instance.user
    if user:
        user.delete()