from django.contrib import admin
from .forms import ObservatoryAdminForm
from django.core.exceptions import ValidationError

from .models import Tbl_observatory, Tbl_telescope, Tbl_instrument

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

admin.site.register(Tbl_observatory, ObservatoryAdmin)


# 'telescope' table
class TelescopeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Telescope information", {"fields": ["fullname", "owner", "obs_tel", "website", "status"]}),
        ("Characteristics", {"fields": ["aperture"]}),
    ]

admin.site.register(Tbl_telescope, TelescopeAdmin)



# 'instrument' table
class InstrumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Instrument information", {"fields": ["fullname", "tel_ins", "website", "status"]}),
    ]

admin.site.register(Tbl_instrument, InstrumentAdmin)