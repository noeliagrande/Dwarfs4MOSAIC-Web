from django.contrib import admin
from .forms import ObservatoryAdminForm
from .models import *

admin.site.site_header = "Dwarfs4MOSAIC Database Administration"

# 'observatory' table
@admin.register(Tbl_observatory)
class ObservatoryAdmin(admin.ModelAdmin):
    form = ObservatoryAdminForm

    empty_value_display = ""  # Shows empty field instead of 'None'

    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": [
            "location", "website",
        ]}),
        ("Coordinates", {"fields": [
            ("longitude_deg", "longitude_min", "longitude_sec", "longitude_ew"),
            ("latitude_deg", "latitude_min", "latitude_sec", "latitude_ns"),
            "altitude"
        ]}),
    ]

# 'telescope' table
@admin.register(Tbl_telescope)
class TelescopeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": ["description", "owner", "obs_tel", "website", "status"]}),
        ("Characteristics", {"fields": ["aperture"]}),
    ]

# 'instrument' table
@admin.register(Tbl_instrument)
class InstrumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": ["description", "tel_ins", "website", "status"]}),
    ]

# 'researcher' table
@admin.register(Tbl_researcher)
class ResearcherAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("General Information", {"fields": ["role", "institution", "email"]}),
    ]

# 'observing_run' table
@admin.register(Tbl_observing_run)
class ObservingRunAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General Information", {"fields": ["name", "description", "instrument", "start_date", "end_date", ]}), #targets
        ("Participants", {"fields": ["researchers"]}),
        ("Additional Data", {"fields": ["notes"]}),
    ]
    filter_horizontal = ['researchers']

# 'observing_block' table
@admin.register(Tbl_observing_block)
class ObservingBlockAdmin(admin.ModelAdmin):
    # Display the researchers of the selected observing_run

    #def formfield_for_manytomany(self, db_field, request, **kwargs):
    #    if db_field.name == 'researchers':
    #        obj_id = request.resolver_match.kwargs.get('object_id')
    #        if obj_id:
    #            obj = Tbl_observing_block.objects.get(pk=obj_id)
    #            kwargs['queryset'] = Tbl_researcher.objects.filter(observing_runs=obj.obs_run)
    #        else:
    #            kwargs['queryset'] = Tbl_researcher.objects.none()
    #    return super().formfield_for_manytomany(db_field, request, **kwargs)

    #class Media:
    #    js = ("dwarfs4MOSAIC/admin/js/observing_block.js",)

    fieldsets = [
        ("General Information", {"fields": ["name", "obs_run", "description", "start_time", "end_time", ]}),
        ("Participants", {"fields": ["researchers"]}),
        ("Observation Information", {"fields": ["observation_mode", "filters", "exposure_time", "seeing", "weather_conditions"]}),  # "target"
        ("Additional Data", {"fields": ["notes"]}),
    ]
    filter_horizontal = ['researchers']

