"""
Django Admin configuration for the Dwarfs4MOSAIC project.

This file defines how each model is displayed and managed in the Django Admin interface.
It includes custom forms, custom file handling logic (images and data files for targets),
and overrides default admin behavior where necessary.
"""

from django.contrib import admin
from .forms import ObservatoryAdminForm, TargetAdminForm
from .models import *
from .utils import sanitize_filename

import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.http import HttpResponseRedirect

# Custom title for the Django Admin interface
admin.site.site_header = "Dwarfs4MOSAIC Administration" # default: Django administration
admin.site.site_title = "Dwarfs4MOSAIC Admin Portal"
# admin.site.index_title = "Site administration" (default)

# --- 'observatory' table ---
@admin.register(Tbl_observatory)
class ObservatoryAdmin(admin.ModelAdmin):
    form = ObservatoryAdminForm
    empty_value_display = ""  # Display empty string instead of 'None'

    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "location", "website",]}),
        ("Coordinates", {"fields": [
            ("longitude_deg", "longitude_min", "longitude_sec", "longitude_ew"),
            ("latitude_deg", "latitude_min", "latitude_sec", "latitude_ns"),
            "altitude"]}),]

# --- 'telescope' table ---
@admin.register(Tbl_telescope)
class TelescopeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "owner", "obs_tel", "website", "status"]}),
        ("Characteristics", {"fields": [
            "aperture"]}),]

# --- 'instrument' table ---
@admin.register(Tbl_instrument)
class InstrumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "tel_ins", "website", "status"]}),]

# --- 'user' admin
class CustomUserAdmin(DefaultUserAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        user = User.objects.filter(pk=object_id).first()
        extra_context = extra_context or {}

        # If the user has a linked researcher, pass its admin change URL
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

# Replace default admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# --- 'researcher' table ---
@admin.register(Tbl_researcher)
class ResearcherAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["user"]}),
        ("General Information", {"fields": [
            'is_phd', 'institution', 'comments']}),
        ("Authorization", {"fields": [
            "allowed_blocks", "allowed_targets"]}), ]

    # Enable horizontal multi-selection widget
    filter_horizontal = ['allowed_blocks', 'allowed_targets']

    # Redirect attempts to add a Researcher to the User admin page.
    def add_view(self, request, form_url='', extra_context=None):
        user_admin_url = reverse('admin:auth_user_add')
        return redirect(user_admin_url)

    def get_fieldsets(self, request, obj=None):
        # Always show 'user', just make it readonly when editing
        return self.fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.user is None:
            # Researcher without linked user → make all fields read-only
            return [f.name for f in self.model._meta.fields] + ['allowed_blocks', 'allowed_targets']
        if obj:
            # Editing a researcher with linked user → make only 'user' field read-only
            return ['user']
        return super().get_readonly_fields(request, obj)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # Add extra context to hide save buttons when user is missing
        extra_context = extra_context or {}
        if object_id:
            researcher = Tbl_researcher.objects.get(pk=object_id)
            # If researcher has no user, disable all save buttons
            if researcher.user is None:
                extra_context['show_save'] = False
                extra_context['show_save_and_add_another'] = False
                extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)

# --- 'observing_run' table ---
@admin.register(Tbl_observing_run)
class ObservingRunAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "instrument", "start_date", "end_date", ]}), #targets
        ("Participants", {"fields": [
            "researchers"]}),
        ("Additional Data", {"fields": [
            "comments"]}),]

    # Enable horizontal multi-selection widget
    filter_horizontal = ['researchers']

# --- 'observing_block' table ---
@admin.register(Tbl_observing_block)
class ObservingBlockAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "obs_run", "description", "start_time", "end_time", ]}),
        ("Observation Information", {"fields": [
            "observation_mode", "filters", "exposure_time", "seeing", "weather_conditions", "target"]}),
        ("Additional Data", {"fields": [
            "comments"]}),]

    # Enable horizontal multi-selection widget
    filter_horizontal = ['target']

# --- 'target' table ---
@admin.register(Tbl_target)
class TargetAdmin(admin.ModelAdmin):

    form = TargetAdminForm

    class Media:
        css = {'all': ('admin/css/widgets.css',)}
        js = ('admin/js/core.js', 'admin/js/SelectBox.js', 'admin/js/SelectFilter2.js',)

    def get_fieldsets(self, request, obj=None):
        base_fieldsets = [
            ("General Information", {"fields": [
                "type", "right_ascension", "declination", "magnitude", "redshift", "size"]}),
            ("Additional Data", {"fields": [
                "semester", "comments",
                ]}),
        ]

        # Show 'name' field when creating a new object
        if obj is None:
            base_fieldsets.insert(0, (None, {"fields": ["name"]}))
            return base_fieldsets

        # Add file upload section only when editing an existing object
        if obj and obj.pk:
            base_fieldsets.append(
                ("Upload Files",
                {
                    "description": "⚠️ Files with the same name will overwrite existing ones.",
                    "fields": [
                        # Show delete checkbox only if there is already an image
                        ("upload_image", "delete_image") if obj.image_name else "upload_image",
                        "upload_datafiles"
                    ]
                })
            )
            base_fieldsets.append(
                ("Delete Data Files", {"fields": ["datafiles"]})
            )

        return base_fieldsets

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None  # True if the object is being created

        super().save_model(request, obj, form, change)

        safe_name = sanitize_filename(obj.name)
        base_path = os.path.join(settings.MEDIA_ROOT, safe_name) # MEDIA_ROOT/target_name
        datafiles_path = os.path.join(base_path, "datafiles")    # MEDIA_ROOT/target_name/datafiles
        image_path = os.path.join(base_path, "image")            # MEDIA_ROOT/target_name/image

        # Ensure directories exist
        os.makedirs(datafiles_path, exist_ok=True)
        os.makedirs(image_path, exist_ok=True)

        if is_new:
            # Save relative paths on first creation
            obj.datafiles_path = os.path.relpath(datafiles_path, settings.MEDIA_ROOT)
            obj.image = os.path.relpath(image_path, settings.MEDIA_ROOT)
            obj.save()
            return

        # Handle image deletion
        if form.cleaned_data.get('delete_image') and obj.image_name:
            image_file_path = os.path.join(settings.MEDIA_ROOT, obj.image)
            if os.path.exists(image_file_path):
                os.remove(image_file_path)

            # Check if image was really deleted
            if os.path.exists(image_file_path):
                self.message_user(
                    request,
                    f'Warning: the image "{obj.image_name}" could not be deleted.',
                    level=messages.WARNING
                )
            else:
                obj.image = os.path.relpath(image_path, settings.MEDIA_ROOT) # Reset to default image relative path

        else:
            # Handle image upload
            upload_image = form.cleaned_data.get('upload_image')
            if upload_image:

                previous_image_name = obj.image_name
                previous_image_path = os.path.join(settings.MEDIA_ROOT, obj.image)

                # Save new image
                file_path = os.path.join(image_path, upload_image.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in upload_image.chunks():
                        destination.write(chunk)

                # Check if the file was actually saved
                if not os.path.isfile(file_path):
                    self.message_user(
                        request,
                        f'Warning: the image "{upload_image.name}" could not be uploaded.',
                        level=messages.WARNING
                    )

                else:
                    obj.image = os.path.relpath(file_path, settings.MEDIA_ROOT) # new image

                    # Delete previous image
                    if previous_image_name and os.path.exists(previous_image_path):
                        os.remove(previous_image_path)

        # Handle multiple file uploads
        datafiles = form.cleaned_data.get("upload_datafiles", [])
        for uploaded_file in datafiles:
            dest_path = os.path.join(datafiles_path, uploaded_file.name)
            with open(dest_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        # Handle datafiles deletion
        files_to_delete = form.cleaned_data.get("datafiles", [])
        for filename in files_to_delete:
            safe_name = os.path.basename(filename)
            file_path = os.path.join(datafiles_path, safe_name)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    self.message_user(
                        request,
                        f'Error deleting file "{filename}": {e}',
                        level=messages.ERROR
                    )

        # Save all changes
        obj.save()

    def get_actions(self, request):
        # Replace default bulk delete action with a custom one
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

    # Override response after adding object to always redirect to change page,
    # except when pressing "Save and add another" (then go to add new).
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

    def get_change_url(self, obj):
        opts = self.model._meta
        return f"/admin/{opts.app_label}/{opts.model_name}/{obj.pk}/change/"