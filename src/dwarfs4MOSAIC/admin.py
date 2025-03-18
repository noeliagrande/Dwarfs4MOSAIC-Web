from django.contrib import admin
from .forms import ObservatoryAdminForm
from . import models

admin.site.site_header = "Dwarfs4MOSAIC Database Administration"

# 'observatory' table
class ObservatoryAdmin(admin.ModelAdmin):
    form = ObservatoryAdminForm

    empty_value_display = ""  # Shows empty field instead of 'None'

    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": ["location", "website"]}),
        ("Longitude", {"fields": ["longitude_ew", "longitude_deg", "longitude_min", "longitude_sec"], "classes": ["collapse"]}),
        ("Latitude", {"fields": ["latitude_ns", "latitude_deg", "latitude_min", "latitude_sec"], "classes": ["collapse"]}),
        (None, {"fields": ["altitude"]}),
    ]

admin.site.register(models.Tbl_observatory, ObservatoryAdmin)


# 'telescope' table
class TelescopeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": ["description", "owner", "obs_tel", "website", "status"]}),
        ("Characteristics", {"fields": ["aperture"]}),
    ]

admin.site.register(models.Tbl_telescope, TelescopeAdmin)


# 'instrument' table
class InstrumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": ["description", "tel_ins", "website", "status"]}),
    ]

admin.site.register(models.Tbl_instrument, InstrumentAdmin)


# 'researcher' table
class ResearcherAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": ["role", "institution", "email"]}),
    ]

admin.site.register(models.Tbl_researcher, ResearcherAdmin)


# 'observing_run' table
class ObservingRunAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General Information", {"fields": ["name", "description", "instrument", "start_date", "end_date", ]}), #targets
        ("Participants", {"fields": []}), # "researchers"
        ("Additional Data", {"fields": ["notes"]}),
    ]

admin.site.register(models.Tbl_observing_run, ObservingRunAdmin)


# 'observing_block' table
class ObservingBlockAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General Information", {"fields": ["name", "obs_run", "description", "start_time", "end_time", ]}),
        ("Participants", {"fields": []}), # "researchers"
        ("Observation Information", {"fields": ["observation_mode", "filters", "exposure_time", "seeing", "weather_conditions"]}),  # "researchers", "target"
        ("Additional Data", {"fields": ["notes"]}),
    ]

admin.site.register(models.Tbl_observing_block, ObservingBlockAdmin)


