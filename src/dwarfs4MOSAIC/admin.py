from django.contrib import admin
from .forms import ObservatoryAdminForm, ResearcherAdminForm
from .models import *

from django.utils.html import format_html
from django.urls import reverse

admin.site.site_header = "Dwarfs4MOSAIC Login"

# 'observatory' table
@admin.register(Tbl_observatory)
class ObservatoryAdmin(admin.ModelAdmin):
    form = ObservatoryAdminForm
    empty_value_display = ""  # Shows empty field instead of 'None'

    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "location", "website",]}),
        ("Coordinates", {"fields": [
            ("longitude_deg", "longitude_min", "longitude_sec", "longitude_ew"),
            ("latitude_deg", "latitude_min", "latitude_sec", "latitude_ns"),
            "altitude"]}),]

# 'telescope' table
@admin.register(Tbl_telescope)
class TelescopeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "owner", "obs_tel", "website", "status"]}),
        ("Characteristics", {"fields": [
            "aperture"]}),]

# 'instrument' table
@admin.register(Tbl_instrument)
class InstrumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "description", "tel_ins", "website", "status"]}),]

# 'researcher' table
@admin.register(Tbl_researcher)
class ResearcherAdmin(admin.ModelAdmin):
    form = ResearcherAdminForm  # Usamos el formulario personalizado

    fieldsets = [
        (None, {"fields": ['user', 'is_phd', 'institution', 'comments']}),
    ]


# 'observing_run' table
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

    filter_horizontal = ['researchers']

# 'observing_block' table
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

    filter_horizontal = ['target']

# 'target' table
@admin.register(Tbl_target)
class TargetAdmin(admin.ModelAdmin):

    readonly_fields = ['current_datafiles_path', 'upload_info', 'upload_button']

    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "type", "right_ascension", "declination", "magnitude", "redshift", "size"]}),
        ("Additional Data", {"fields": [
            "semester", "comments",
            "image", 'datafiles_path']}),
        ("Upload Data Files", {"fields": [
            'upload_info', 'current_datafiles_path', 'upload_button']}),
    ]

    def current_image(self, obj):
        return obj.image or "(No image set)"

    current_image.short_description = "Current image"

    def current_datafiles_path(self, obj):
        return obj.datafiles_path or "(No datafiles path set)"

    current_datafiles_path.short_description = "Current datafiles path"

    def upload_info(self, obj):
        return format_html(
            "Files will be uploaded to the path shown in <strong style='color:red;'>‘Current datafiles path’</strong>.<br>"
            "Please set a valid path and click <strong>‘Save and continue editing’</strong> to apply the changes before uploading."
        )

    upload_info.short_description = "IMPORTANT"

    def upload_button(self, obj):
        if obj.pk:
            url = reverse('upload_files_view', args=[obj.pk])
            disabled = not bool(obj.datafiles_path and obj.datafiles_path.strip())
            if disabled:
                return format_html(
                    '<button type="button" disabled style="opacity:0.5; cursor:not-allowed;">Upload Files</button>'
                )
            else:
                return format_html(
                    '<a class="button" href="{}">Upload Files</a>', url
                )
        return "Save and reload to upload files"

    upload_button.short_description = "Upload data files"
