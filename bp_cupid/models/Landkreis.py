from django.db import models

class Landkreis(models.Model):
    plz_von = models.IntegerField(
        default=0,
        verbose_name='von'
    )
    plz_bis = models.IntegerField(
        default=0,
        verbose_name='bis'
    )
    name = models.CharField(
        max_length=100,
        default='',
        verbose_name='Name'
    )
    orte = models.CharField(
        max_length=200,
        default='',
        verbose_name='Orte'
    )

    class Meta:
        verbose_name = 'Landkreis'
        verbose_name_plural = 'Landkreise'

    def __str__(self):
        return self.name
