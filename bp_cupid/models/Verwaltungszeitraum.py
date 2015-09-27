from django.db import models
from datetime import date

class Verwaltungszeitraum(models.Model):
    """
    Ein Verwaltungszeitraum ist dem Semester übergeordnet. Ein Student kann das
    BP im Winter- oder im Sommersemester ableisten. Wir müssen aber beide
    Semester in einem Rutsch verwalten.
    """
    name = models.CharField(
        max_length=50,
        unique=True
    )
    anfang = models.DateField()
    ende = models.DateField()

    def aktuell():
        """
        Gibt den aktuellen Verwaltungszeitraum zurück.
        """
        today = date.today()
        return Verwaltungszeitraum.objects.filter(
            anfang__lte=today, ende__gte=today,
        ).first()

    def maximale_kapazitaet(self):
        return sum(b.maximale_kapazitaet() for b in self.bloecke.all())

    class Meta:
        verbose_name = 'Verwaltungszeitraum'
        verbose_name_plural = 'Verwaltungszeiträume'

    def __str__(self):
        return self.name
