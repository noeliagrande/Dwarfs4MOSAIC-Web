"""
Django Admin configuration for the Dwarfs4MOSAIC project.

This file defines how each model is displayed and managed in the Django Admin interface.
It includes custom forms, custom file handling logic (images and data files for targets),
and overrides default admin behavior where necessary.
"""

# Standard libraries
import os

# Third-party libraries
from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as DefaultGroupAdmin, UserAdmin as DefaultUserAdmin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

# Local application imports
from .forms import GroupAdminForm, ObservatoryAdminForm, TargetAdminForm
from .models import *
from .utils import sanitize_filename


# Set custom header and title for the admin site
admin.site.site_header = "Dwarfs4MOSAIC Administration" # default: Django administration
admin.site.site_title = "Dwarfs4MOSAIC Admin Portal"
# admin.site.index_title = "Site administration" (default)

# Replace default Group admin with custom form and fieldsets
admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(DefaultGroupAdmin):
    form = GroupAdminForm

    # Define fields and additional authorization fields
    fieldsets = (
        (None, {'fields': ('name', 'permissions')}),
        ('Authorization', {'fields': ('allowed_blocks',)}),
    )

# Admin configuration for the Observatory model
@admin.register(Tbl_observatory)
class ObservatoryAdmin(admin.ModelAdmin):
    form = ObservatoryAdminForm
    empty_value_display = ""  # Show empty string instead of None

    # Organize fields into sections
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "location", "website",]}),
        ("Coordinates", {"fields": [
            ("longitude_deg", "longitude_min", "longitude_sec", "longitude_ew"),
            ("latitude_deg", "latitude_min", "latitude_sec", "latitude_ns"),
            "altitude"]}),]

# Admin configuration for the Telescope model
@admin.register(Tbl_telescope)
class TelescopeAdmin(admin.ModelAdmin):
    # Organize fields into sections
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "owner", "obs_tel", "website", "status"]}),
        ("Characteristics", {"fields": [
            "aperture"]}),]

# Admin configuration for the Instrument model
@admin.register(Tbl_instrument)
class InstrumentAdmin(admin.ModelAdmin):
    # Organize fields into sections
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "tel_ins", "website", "status"]}),]

# Custom User admin to add link to linked Researcher if exists
class CustomUserAdmin(DefaultUserAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        user = User.objects.filter(pk=object_id).first()
        extra_context = extra_context or {}

        # Add link to Researcher admin page if user has linked researcher
        try:
            researcher = user.researcher
            researcher_url = reverse(
                'admin:dwarfs4MOSAIC_tbl_researcher_change',
                args=[researcher.pk]
            )
            extra_context['researcher_link'] = researcher_url
        except Tbl_researcher.DoesNotExist:
            extra_context['researcher_link'] = None

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

# Replace default User admin with custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Admin configuration for the Researcher model
@admin.register(Tbl_researcher)
class ResearcherAdmin(admin.ModelAdmin):
    # Organize fields into sections
    fieldsets = [
        (None, {"fields": ['user', 'role']}),
        ("General Information", {"fields": [
            'is_phd', 'institution', 'comments']}),
        ("Authorization", {"fields": [
            "denied_blocks"]}),
    ]

    # Multi-select widget for denied_blocks
    filter_horizontal = ['denied_blocks']

    # Redirect adding a Researcher to User creation page
    def add_view(self, request, form_url='', extra_context=None):
        user_admin_url = reverse('admin:auth_user_add')
        return redirect(user_admin_url)

    # Always show user field, just make it readonly when editing.
    def get_fieldsets(self, request, obj=None):
        return self.fieldsets

    # Customize read-only fields
    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.user is None:
            # If no linked user, make all fields read-only
            return [f.name for f in self.model._meta.fields] + ['denied_blocks']
        if obj:
            # When editing with linked user, make only 'user' read-only
            return ['user']
        return super().get_readonly_fields(request, obj)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # Hide save buttons if researcher has no linked user
        extra_context = extra_context or {}
        if object_id:
            researcher = Tbl_researcher.objects.get(pk=object_id)
            if researcher.user is None:
                extra_context['show_save'] = False
                extra_context['show_save_and_add_another'] = False
                extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)

# Admin configuration for Observing Run model
@admin.register(Tbl_observing_run)
class ObservingRunAdmin(admin.ModelAdmin):
    # Organize fields into sections
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "instrument", "start_date", "end_date", ]}), #targets
        ("Participants", {"fields": [
            "researchers"]}),
        ("Additional Data", {"fields": [
            "comments"]}),]

    # Multi-select widget for researchers
    filter_horizontal = ['researchers']

# Admin configuration for Observing Block model
@admin.register(Tbl_observing_block)
class ObservingBlockAdmin(admin.ModelAdmin):
    # Organize fields into sections
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "obs_run", "description", "start_time", "end_time", ]}),
        ("Observation Information", {"fields": [
            "observation_mode", "filters", "exposure_time", "seeing", "weather_conditions", "target"]}),
        ("Additional Data", {"fields": [
            "comments"]}),]

    # Multi-select widget for targets
    filter_horizontal = ['target']

# Admin configuration for Target model with custom file handling
@admin.register(Tbl_target)
class TargetAdmin(admin.ModelAdmin):

    # Custom form with file upload fields
    form = TargetAdminForm

    # Include necessary CSS and JS for admin widgets
    class Media:
        css = {'all': ('admin/css/widgets.css',)}
        js = ('admin/js/core.js', 'admin/js/SelectBox.js', 'admin/js/SelectFilter2.js',)

    def get_fieldsets(self, request, obj=None):
        # Organize fields into sections
        base_fieldsets = [
            ("General Information", {"fields": [
                "type", "right_ascension", "declination", "magnitude", "redshift", "size"]}),
            ("Additional Data", {"fields": [
                "semester", "comments",
                ]}),
        ]

        # When creating new Target, show 'name' field
        if obj is None:
            base_fieldsets.insert(0, (None, {"fields": ["name"]}))
            return base_fieldsets

        # When editing existing Target, add file upload and deletion sections
        if obj and obj.pk:
            base_fieldsets.append(
                ("Upload Files",
                {
                    "description": "⚠️ Files with the same name will overwrite existing ones.",
                    "fields": [
                        "upload_image", "upload_datafiles"
                    ]
                })
            )
            base_fieldsets.append(
                ("Delete Files", {
                    "fields": ["delete_image", "datafiles"]
                })
            )

        return base_fieldsets

    def save_model(self, request, obj, form, change):
        # Detect if the object is new (being created)
        is_new = obj.pk is None

        # Save the model normally first
        super().save_model(request, obj, form, change)

        # Define safe filesystem paths for storing files related to this target
        safe_name = sanitize_filename(obj.name)
        base_path = os.path.join(settings.MEDIA_ROOT, safe_name) # Base folder: MEDIA_ROOT/target_name
        datafiles_path = os.path.join(base_path, "datafiles")    # Folder for data files: MEDIA_ROOT/target_name/datafiles
        image_path = os.path.join(base_path, "image")            # Folder for image file: MEDIA_ROOT/target_name/image

        # Create directories if they do not exist
        os.makedirs(datafiles_path, exist_ok=True)
        os.makedirs(image_path, exist_ok=True)

        if is_new:
            # For new objects, store relative paths and save again
            obj.datafiles_path = os.path.relpath(datafiles_path, settings.MEDIA_ROOT)
            obj.image = os.path.relpath(image_path, settings.MEDIA_ROOT)
            obj.save()
            return

        # Delete image if requested and exists
        if form.cleaned_data.get('delete_image') and obj.image_name:
            image_file_path = os.path.join(settings.MEDIA_ROOT, obj.image)
            if os.path.exists(image_file_path):
                os.remove(image_file_path)

            # Check if deletion succeeded
            if os.path.exists(image_file_path):
                # Show warning if image could not be deleted
                self.message_user(
                    request,
                    f'Warning: the image "{obj.image_name}" could not be deleted.',
                    level=messages.WARNING
                )
            else:
                # Reset image path to default folder
                obj.image = os.path.relpath(image_path, settings.MEDIA_ROOT) # Reset to default image relative path

        else:
            # Handle image upload if provided
            upload_image = form.cleaned_data.get('upload_image')
            if upload_image:

                previous_image_name = obj.image_name
                previous_image_path = os.path.join(settings.MEDIA_ROOT, obj.image)

                # Save uploaded image to disk
                file_path = os.path.join(image_path, upload_image.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in upload_image.chunks():
                        destination.write(chunk)

                if not os.path.isfile(file_path):
                    # Warn if upload failed
                    self.message_user(
                        request,
                        f'Warning: the image "{upload_image.name}" could not be uploaded.',
                        level=messages.WARNING
                    )

                else:
                    # Update image path to new file
                    obj.image = os.path.relpath(file_path, settings.MEDIA_ROOT) # new image

                    # Remove old image file if it exists
                    if previous_image_name and os.path.exists(previous_image_path):
                        os.remove(previous_image_path)

        # Save multiple data files uploaded by user
        datafiles = form.cleaned_data.get("upload_datafiles", [])
        for uploaded_file in datafiles:
            dest_path = os.path.join(datafiles_path, uploaded_file.name)
            with open(dest_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        # Delete selected data files if requested
        files_to_delete = form.cleaned_data.get("datafiles", [])
        for filename in files_to_delete:
            safe_name = os.path.basename(filename)
            file_path = os.path.join(datafiles_path, safe_name)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    # Show error message if deletion fails
                    self.message_user(
                        request,
                        f'Error deleting file "{filename}": {e}',
                        level=messages.ERROR
                    )

        # Save the model instance after file operations
        obj.save()

    def get_actions(self, request):
        # Override default bulk delete action with a custom version
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            actions["delete_selected"] = (
                self.custom_delete_selected,
                *actions["delete_selected"][1:]
            )
        return actions

    def custom_delete_selected(self, modeladmin, request, queryset):
        # Delete selected objects and show a summary message
        deleted_count = 0
        for obj in queryset:
            obj.delete()
            deleted_count += 1
        self.message_user(
            request,
            f" {deleted_count} target(s) and their associated folders were deleted.",
            level=messages.SUCCESS,
        )

    # Override response after adding object: redirect to change page,
    # except when using "Save and add another" (then redirect to add new)
    def response_add(self, request, obj, post_url_continue=None):
        if "_addanother" in request.POST:
            # Default behaviour for 'Save and add another' (go to add new)
            return super().response_add(request, obj, post_url_continue)
        elif "_continue" in request.POST or "_save" in request.POST:
            # For both 'Save and continue editing' and 'Save',
            # redirect to the change page of the newly created object
            url = self.get_change_url(obj)
            return HttpResponseRedirect(url)
        else:
            return super().response_add(request, obj, post_url_continue)

    # Build URL for change page of this object in admin
    def get_change_url(self, obj):
        opts = self.model._meta
        return f"/admin/{opts.app_label}/{opts.model_name}/{obj.pk}/change/"