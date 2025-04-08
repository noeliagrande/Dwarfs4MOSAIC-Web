
from django.contrib.auth.models import User, Group
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver

from .models import Tbl_target, Tbl_instrument, Tbl_researcher

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


# Create group when an instance is created
def create_or_update_group(instance, model):
    try:
        # if the object already exists (it is not a new object)
        old_instance = Tbl_target.objects.get(pk=instance.pk)

        if old_instance.name != instance.name:
            # If the target's name has changed, we update the group
            try:
                old_group = Group.objects.get(name=old_instance.name)

                # Create the new group with the new name
                new_group, created = Group.objects.get_or_create(name=instance.name)

                # Reassign users to new group
                users_in_old_group = old_group.user_set.all()
                for user in users_in_old_group:
                    user.groups.remove(old_group)
                    user.groups.add(new_group)
                    user.save()

                old_group.delete()

            except Group.DoesNotExist:
                # If the group did not exist, we create it with the new name
                Group.objects.get_or_create(name=instance.name)

    except Tbl_target.DoesNotExist:
        # If the target is new, create the group
        Group.objects.get_or_create(name=instance.name)


# Create group when a target or instrument is created
@receiver(pre_save, sender=Tbl_target)
@receiver(pre_save, sender=Tbl_instrument)
def create_or_update_group_for_instance(sender, instance, **kwargs):
    create_or_update_group(instance, sender)


# Delete group when an instance is deleted
def delete_group_if_exists(instance):
    try:
        group = Group.objects.get(name=instance.name)
        group.delete()
    except Group.DoesNotExist:
        pass

# Delete group when a target or instrument is deleted
@receiver(post_delete, sender=Tbl_target)
@receiver(post_delete, sender=Tbl_instrument)
def delete_group_for_instance(sender, instance, **kwargs):
    delete_group_if_exists(instance)



