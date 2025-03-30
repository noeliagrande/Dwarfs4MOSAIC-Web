from django.contrib import admin
from .forms import ObservatoryAdminForm
from .models import *

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
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "role", "institution", "email"]}),]

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
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "type", "right_ascension", "declination", "magnitude", "redshift", "size"]}),
        ("Additional Data", {"fields": [
            "semester", "comments", 'image']}),]