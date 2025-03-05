from django.contrib import admin

from .models import Tbl_observatory, Tbl_telescope, Tbl_instrument

# Register your models here.
admin.site.register(Tbl_observatory)
admin.site.register(Tbl_telescope)
admin.site.register(Tbl_instrument)