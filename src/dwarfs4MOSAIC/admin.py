from django.contrib import admin
from .forms import ObservatoryAdminForm, ResearcherAdminForm, TargetAdminForm
from .models import *

from django.utils.html import format_html
from django.urls import reverse

from .utils import sanitize_filename

import os
from django.conf import settings
from django.contrib import messages

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

    form = TargetAdminForm

    def get_readonly_fields(self, request, obj=None):
        base_readonly = []
        if obj:  # el objeto ya existe
            return ['name'] + base_readonly
        return base_readonly

    def get_fieldsets(self, request, obj=None):
        base_fieldsets = [
            (None, {"fields": ["name"]}),
            ("General Information", {"fields": [
                "type", "right_ascension", "declination", "magnitude", "redshift", "size"]}),
            ("Additional Data", {"fields": [
                "semester", "comments",
                ]}),
        ]

        # Solo añadir la sección de subida si el objeto ya existe (edición)
        if obj and obj.pk:
            base_fieldsets.append(
                ("Upload Files", {"fields": [
                    'upload_image', 'upload_datafiles'
                ]})
            )

        return base_fieldsets

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None  # True si se está creando por primera vez

        super().save_model(request, obj, form, change)

        #safe_name = sanitize_filename(obj.name)
        #base_path = os.path.join(settings.MEDIA_ROOT, safe_name)
        base_path = obj.absolute_path
        datafiles_path = os.path.join(base_path, "datafiles")
        image_path = os.path.join(base_path, "image")

        # Asegúrate de que las carpetas existen
        os.makedirs(datafiles_path, exist_ok=True)
        os.makedirs(image_path, exist_ok=True)

        if is_new:
            ''' ESTO NO SERÁ NECESARIO? '''
            # Obtener ruta relativa respecto al directorio base del proyecto
            relative_datafiles_path = os.path.relpath(datafiles_path, start=settings.BASE_DIR)
            #obj.datafiles_path = relative_datafiles_path
            obj.datafiles_path = datafiles_path

            #obj.image = ""
            obj.image = image_path
            ''' ESTO NO SERÁ NECESARIO '''

            # Guardar paths
            obj.save()

        if not is_new:
            upload_image = form.cleaned_data.get('upload_image')
            if upload_image:
                file_path = os.path.join(image_path, upload_image.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in upload_image.chunks():
                        destination.write(chunk)

                relative_image_path = os.path.relpath(image_path, start=settings.BASE_DIR)
                #obj.image = os.path.join(relative_image_path, upload_image.name)
                obj.image = os.path.join(image_path, upload_image.name)
                obj.save()

            # Al final: comprobar si el archivo realmente se guardó
            if obj.image and not os.path.isfile(os.path.join(settings.BASE_DIR, obj.image)):
                self.message_user(
                    request,
                    f'⚠️ Warning: the image file "{obj.image}" does not exist on disk.',
                    level=messages.WARNING
                )

            datafiles = form.cleaned_data.get("upload_datafiles", [])
            for uploaded_file in datafiles:
                dest_path = os.path.join(datafiles_path, uploaded_file.name)
                with open(dest_path, "wb+") as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

