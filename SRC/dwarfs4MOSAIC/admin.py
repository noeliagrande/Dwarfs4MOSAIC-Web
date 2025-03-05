from django.contrib import admin

from .models import Tbl_observatory, Tbl_telescope, Tbl_instrument

admin.site.site_header = "Dwarfs4MOSAIC Database Administration"

# 'observatory' table
class ObservatoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Observatory information", {"fields": []}),
    ]

admin.site.register(Tbl_observatory, ObservatoryAdmin)


# 'telescope' table
class TelescopeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Telescope information", {"fields": ["obs_tel"]}),
    ]

admin.site.register(Tbl_telescope, TelescopeAdmin)



# 'instrument' table
class InstrumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Instrument information", {"fields": ["tel_ins"]}),
    ]

admin.site.register(Tbl_instrument, InstrumentAdmin)