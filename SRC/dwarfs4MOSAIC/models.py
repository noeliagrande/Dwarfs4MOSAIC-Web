from django.db import models

'''
Table 'observatory'
- name: observatory name
'''
class Tbl_observatory(models.Model):
    name = models.CharField(max_length=200, default="")

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
    name = models.CharField(max_length=200, default="")
    obs_tel = models.ForeignKey(Tbl_observatory, on_delete = models.CASCADE)

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
    name = models.CharField(max_length=200, default="")
    tel_ins = models.ForeignKey(Tbl_telescope, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"