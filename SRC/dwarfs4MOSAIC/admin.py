from django.contrib import admin

from .models import observatory, telescope, instrument

# Register your models here.
admin.site.register(observatory)
admin.site.register(telescope)
admin.site.register(instrument)