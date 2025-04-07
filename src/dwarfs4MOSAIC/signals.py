
from django.contrib.auth.models import User, Group
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver

from .models import Tbl_observatory, Tbl_researcher

# Create group when creating observatory
@receiver(pre_save, sender=Tbl_observatory)
def create_or_update_group_for_observatory(sender, instance, **kwargs):
    try:
        # if the object already exists (it is not a new object)
        old_instance = Tbl_observatory.objects.get(pk=instance.pk)

        if old_instance.name != instance.name:
            # If the observatory's name has changed, we update the group
            try:
                old_group = Group.objects.get(name=old_instance.name)

                # Create the new group with the new name
                new_group, created = Group.objects.get_or_create(name=instance.name)

                # Reasignar usuarios al nuevo grupo
                users_in_old_group = old_group.user_set.all()
                for user in users_in_old_group:
                    user.groups.remove(old_group)  # Remove the user from the old group
                    user.groups.add(new_group)  # Add the user to the new group
                    user.save()

                old_group.delete() # Remove old group

            except Group.DoesNotExist:
                # If the group did not exist, we create it with the new name
                Group.objects.get_or_create(name=instance.name)

    except Tbl_observatory.DoesNotExist:
        # If the observatory is new, create the group
        Group.objects.get_or_create(name=instance.name)

# Delete group when deleting observatory
@receiver(post_delete, sender=Tbl_observatory)
def delete_group_for_observatory(sender, instance, **kwargs):
    try:
        group = Group.objects.get(name=instance.name)
        group.delete()
    except Group.DoesNotExist:
        pass  # If group no longer exists, nothing happens.

# Update researcher when user is changed
@receiver(post_save, sender=User)
def update_researcher(sender, instance, **kwargs):
    try:
        researcher = instance.researcher
        researcher.name = f"{instance.first_name} {instance.last_name}".strip()
        researcher.email = instance.email
        researcher.save()
    except Tbl_researcher.DoesNotExist:
        pass  # If no researcher is associated, nothing is done.