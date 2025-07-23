"""
This file contains the Django model that represents a researcher in the project,
such as a galaxy, calibration source, or other object.
This model defines the database schema, relationships, and basic
behaviors for managing astronomical observation data.
"""

# Third-party libraries
from django.contrib.auth.models import User
from django.db import models

class Tbl_researcher(models.Model):

    # Links the researcher to a Django User object (auth_user)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,  # if User is deleted, the researcher remains
        related_name='researcher',
        verbose_name="Username",
        null=True,
        blank=True,
    )

    # Full name of the researcher
    name = models.CharField(
        max_length=200,
        verbose_name="Name")

    # Optional email address of the researcher
    email = models.EmailField(
        blank=True,
        verbose_name="email")

    # Role of the researcher in the project
    role = models.CharField(
        choices=[
            ('core_team', 'Core Team'),
            ('collaborator', 'Collaborator')],
        max_length=15,  # must be long enough to hold the longest choice
        default='collaborator',
        null=False,
        verbose_name="Role")

    # Institutional affiliation of the researcher
    institution = models.CharField(
        max_length=200,
        default="",
        null=True,
        blank=True,
        verbose_name="Institution")

    # Indicates whether the researcher is a PhD
    is_phd = models.BooleanField(
        default=False,
        verbose_name="Is PhD")

    # Additional notes or comments about the researcher
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comments")

    # Observing runs: Many-to-many relationship is defined in Tbl_observing_run.
    # Django automatically creates reverse accessors.

    # Observing blocks denied to this researcher
    denied_blocks = models.ManyToManyField(
        'Tbl_observing_block',
        blank=True,
        help_text="The user does not have authorized access to these blocks "
                  "(even if they belong to a group that does have authorized access). ",
        related_name='denied_researchers'
    )

    @property
    def display_name(self):
        # Returns the researcher's name, or a placeholder if not set
        return self.name or "(Name not assigned)"

    def __str__(self):
        # Returns a string representation of the researcher
        if self.name:
            return self.name
        elif self.user:
            return self.user.username
        return "(Unnamed Researcher)"

    class Meta:
        # Meta options for admin interface and query ordering
        verbose_name = "Researcher"
        verbose_name_plural = "Researchers"
        ordering = ['user__username']

