"""
Signal handlers for synchronizing Django User and custom model Tbl_researcher.

This module listens to creation or update events on User model to:
- Update related Tbl_researcher fields when a User is updated.
"""

# Third-party libraries
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

# Local application imports
from .models import Tbl_researcher


# Create a Tbl_researcher automatically when a new User is created,
# except if the User is a superuser.
@receiver(post_save, sender=User)
def create_researcher_for_new_user(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        # Create a Tbl_researcher linked to the User instance
        Tbl_researcher.objects.create(
            user=instance,
            name=f"{instance.first_name} {instance.last_name}".strip(),
            email=instance.email,
        )


# When a User is saved, update the linked Tbl_researcher fields
# to keep name and email synchronized.
# If no Tbl_researcher exists, do nothing.
@receiver(post_save, sender=User)
def update_researcher(sender, instance, **kwargs):
    try:
        researcher = instance.researcher
        researcher.name = f"{instance.first_name} {instance.last_name}".strip()
        researcher.email = instance.email
        researcher.save()
    except Tbl_researcher.DoesNotExist:
        pass  # No linked researcher found; do nothing

# When a Tbl_researcher is deleted, also delete its linked User.
@receiver(post_delete, sender=Tbl_researcher)
def delete_user_with_researcher(sender, instance, **kwargs):
    user = instance.user
    if user:
        user.delete()