"""
This file defines how Tbl_target model is displayed and managed in the Django Admin interface.
"""

# Standard libraries
import os

# Third-party libraries
from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path

# Local application imports
from ..forms import TargetAdminForm
from ..forms.form_import_csv import CsvImportForm
from ..models import Tbl_target
from ..utils import sanitize_filename, import_csv_file

# Process each row of the CSV when importing observatories
def process_target_row(row, idx, errors):
    # Required fields: name, semester
    name = row.get("name")
    semester = row.get("semester")

    if not name:
        errors.append(f"Row {idx}: 'name' field is empty, skipping")
        return None

    if not semester:
        errors.append(f"Row {idx}: 'semester' field is empty, skipping")
        return None

    # Build relative paths for image and datafiles based on the target name (safe filename)
    safe_name = sanitize_filename(name)
    base_path = os.path.join(settings.MEDIA_ROOT, safe_name)
    image_path = os.path.join(base_path, "image")
    datafiles_path = os.path.join(base_path, "datafiles")

    # Create directories if they do not exist
    os.makedirs(datafiles_path, exist_ok=True)
    os.makedirs(image_path, exist_ok=True)

    image = row.get("image")
    image_file_path = os.path.join(image_path, image)

    # Prepare defaults
    defaults = {
        "type": row.get("type", "galaxy"),  # default defined in model
        "right_ascension": row.get("right_ascension") or None,
        "declination": row.get("declination") or None,
        "magnitude": None,
        "redshift": None,
        "size": None,
        "semester": semester,
        "comments": row.get("comments", ""),
        "image": os.path.relpath(image_file_path, settings.MEDIA_ROOT),
        "datafiles_path": os.path.relpath(datafiles_path, settings.MEDIA_ROOT),
    }

    # Parse float fields (magnitude, redshift, size)
    for field in ["magnitude", "redshift", "size"]:
        value_str = row.get(field)
        if value_str:
            try:
                defaults[field] = float(value_str)
            except ValueError:
                errors.append(f"Row {idx}: invalid {field} '{value_str}', ignoring")
                defaults[field] = None

    # Create or update the target by unique name
    obj, created_flag = Tbl_target.objects.update_or_create(
        name=name,
        defaults=defaults,
    )

    return created_flag


# Register the Tbl_target model in the admin with custom settings
@admin.register(Tbl_target)
class TargetAdmin(admin.ModelAdmin):

    # Custom form with file upload fields
    form = TargetAdminForm

    # Include necessary CSS and JS for admin widgets
    class Media:
        css = {'all': ('admin/css/widgets.css',)}
        js = ('admin/js/core.js', 'admin/js/SelectBox.js', 'admin/js/SelectFilter2.js',)

    # Group fields into sections in the admin form
    def get_fieldsets(self, request, obj=None):
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
                    "description": "⚠️ On save, files are deleted before new uploads occur.",
                    "fields": ["delete_image", "datafiles"]
                })
            )

        return base_fieldsets

    # On save, selected files (old ones) are deleted before new uploads occur.
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

        # Save multiple data files uploaded by user
        datafiles = form.cleaned_data.get("upload_datafiles", [])
        for uploaded_file in datafiles:
            dest_path = os.path.join(datafiles_path, uploaded_file.name)
            with open(dest_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        # Save the model instance after file operations
        obj.save()

    # Override default bulk delete action with a custom version
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            actions["delete_selected"] = (
                self.custom_delete_selected,
                *actions["delete_selected"][1:]
            )
        return actions

    # Delete selected objects and show a summary message
    def custom_delete_selected(self, modeladmin, request, queryset):

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


    # Override the change list template to add the custom "Import CSV" button
    change_list_template = "admin/dwarfs4MOSAIC/tbl_target_changelist.html"

    # Add a custom URL for CSV import view
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='tbl_target_import_csv'),
        ]
        return custom_urls + urls

    # Handle CSV upload and import using a helper function
    def import_csv(self, request):
        return import_csv_file(
            request,
            CsvImportForm,
            Tbl_target,
            process_target_row,
            title="Import targets from CSV"
        )