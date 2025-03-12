from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

'''
__str__(self): shows how information is displayed when accessing an object from admin
'''


'''
Table 'observatory'
- name: observatory name
'''
class Tbl_observatory(models.Model):
    name = models.CharField(max_length=200, verbose_name = "Name")
    location = models.CharField(max_length=200, verbose_name="Location", default="")

    # Coordinates: when displayed, convert to DEG, MIN, SEC E/W
    longitude = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Observatory"
        verbose_name_plural = "Observatories"

'''
Table 'telescope'
- name: telescope name
- obs_tel: observatory where the telescope is located
'''
class Tbl_telescope(models.Model):
    name = models.CharField(max_length=200, verbose_name = "Name")
    obs_tel = models.ForeignKey(Tbl_observatory, on_delete = models.CASCADE, verbose_name = "Observatory")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Telescope"
        verbose_name_plural = "Telescopes"

'''
Table 'instrument'
- name: instrument name
- tel_ins: telescope where the instrument stands
'''
class Tbl_instrument(models.Model):
    name = models.CharField(max_length=200, verbose_name = "Name")
    tel_ins = models.ForeignKey(Tbl_telescope, on_delete = models.CASCADE, verbose_name = "Telescope")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"