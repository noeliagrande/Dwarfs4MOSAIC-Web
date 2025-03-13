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
        ("Observatory information", {"fields": ["location", "website"]}),
        ("Longitude", {"fields": ["longitude_ew", "longitude_deg", "longitude_min", "longitude_sec"], "classes": ["collapse"]}),
        ("Latitude", {"fields": ["latitude_ns", "latitude_deg", "latitude_min", "latitude_sec"], "classes": ["collapse"]}),
        (None, {"fields": ["altitude"]}),
    ]

admin.site.register(models.Tbl_observatory, ObservatoryAdmin)


# 'telescope' table
class TelescopeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Telescope information", {"fields": ["description", "owner", "obs_tel", "website", "status"]}),
        ("Characteristics", {"fields": ["aperture"]}),
    ]

admin.site.register(models.Tbl_telescope, TelescopeAdmin)



# 'instrument' table
class InstrumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Instrument information", {"fields": ["description", "tel_ins", "website", "status"]}),
    ]

admin.site.register(models.Tbl_instrument, InstrumentAdmin)


# 'member' table
class MemberAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Member information", {"fields": ["role", "institution", "email"]}),
    ]

admin.site.register(models.Tbl_member, MemberAdmin)