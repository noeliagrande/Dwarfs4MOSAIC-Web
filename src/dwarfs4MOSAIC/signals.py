from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Tbl_observatory

# Create group when creating observatory
@receiver(post_save, sender=Tbl_observatory)
def create_group_for_observatory(sender, instance, created, **kwargs):
    if created:
        group_name = instance.name
        Group.objects.get_or_create(name=group_name)

# Delete group when deleting observatory
@receiver(post_delete, sender=Tbl_observatory)
def delete_group_for_observatory(sender, instance, **kwargs):
    try:
        group = Group.objects.get(name=instance.name)
        group.delete()
    except Group.DoesNotExist:
        pass  # If group no longer exists, nothing happens.