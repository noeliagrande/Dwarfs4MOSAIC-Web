"""
Signal handlers for synchronizing Django User, Group, and custom models Tbl_target,
Tbl_instrument, and Tbl_researcher.

This module listens to creation, update, and deletion events on User, Tbl_target,
and Tbl_instrument models to:
- Update related Tbl_researcher fields when a User is updated.
- Create or update Groups matching the names of Tbl_target and Tbl_instrument instances.
- Delete Groups when corresponding Tbl_target or Tbl_instrument instances are deleted.

This ensures consistency between model instances and Django's authentication groups.
"""

from django.contrib.auth.models import User, Group
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver

from .models import Tbl_target, Tbl_instrument, Tbl_researcher

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


# Create or update a Django Group whose name matches the instance's name.
# If the instance is being updated and the name changed:
#     - Find the old group matching the old name.
#     - Create a new group with the new name (or get existing).
#     - Reassign users from old group to new group.
#     - Delete the old group.
# If the instance is new, simply create or get the group with the instance name.
def create_or_update_group(instance, model):
    try:
        # If the object already exists, try to get the existing instance from the database
        old_instance = Tbl_target.objects.get(pk=instance.pk)

        if old_instance.name != instance.name:
            # If the target's name has changed, update group accordingly
            try:
                old_group = Group.objects.get(name=old_instance.name)

                # Create the new group with the new name
                new_group, created = Group.objects.get_or_create(name=instance.name)

                # Reassign users from old group to new group
                users_in_old_group = old_group.user_set.all()
                for user in users_in_old_group:
                    user.groups.remove(old_group)
                    user.groups.add(new_group)
                    user.save()

                # Delete the old group after reassignment
                old_group.delete()

            except Group.DoesNotExist:
                # If old group does not exist, create new group if needed with the new name
                Group.objects.get_or_create(name=instance.name)

    except model.DoesNotExist:
        # New instance, create group with instance name
        Group.objects.get_or_create(name=instance.name)


# Create group when a target or instrument is created
# Signal receiver for pre_save on Tbl_target and Tbl_instrument.
# Calls create_or_update_group to keep Group names synchronized
# with instance names before saving.
@receiver(pre_save, sender=Tbl_target)
@receiver(pre_save, sender=Tbl_instrument)
def create_or_update_group_for_instance(sender, instance, **kwargs):
    create_or_update_group(instance, sender)


# Delete the Django Group whose name matches the instance's name, if it exists.
# Silently passes if no such Group exists.
def delete_group_if_exists(instance):
    try:
        group = Group.objects.get(name=instance.name)
        group.delete()
    except Group.DoesNotExist:
        pass


# Signal receiver for post_delete on Tbl_target and Tbl_instrument.
# Deletes the corresponding Group when the instance is deleted.
@receiver(post_delete, sender=Tbl_target)
@receiver(post_delete, sender=Tbl_instrument)
def delete_group_for_instance(sender, instance, **kwargs):
    delete_group_if_exists(instance)



