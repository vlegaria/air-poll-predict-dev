from django.db import models

# Create your models here.

class PED_NORM(models.Model):
    idData = models.AutoField(primary_key=True)
    date = models.DateField()
    CO = models.DecimalField(max_digits=13, decimal_places=12)
    NO = models.DecimalField(max_digits=13, decimal_places=12)
    NOX = models.DecimalField(max_digits=13, decimal_places=12)
    NO2 = models.DecimalField(max_digits=13, decimal_places=12)
    O3 = models.DecimalField(max_digits=13, decimal_places=12)
    PM10 = models.DecimalField(max_digits=13, decimal_places=12)
    PM25 = models.DecimalField(max_digits=13, decimal_places=12)
    RH = models.DecimalField(max_digits=3, decimal_places=2)
    SO2 = models.DecimalField(max_digits=13, decimal_places=12)
    TMP = models.DecimalField(max_digits=13, decimal_places=12)
    WDR = models.DecimalField(max_digits=13, decimal_places=12)
    WSP = models.DecimalField(max_digits=13, decimal_places=12)
    year = models.IntegerField()
    day = models.IntegerField()
    hora = models.IntegerField()
    minutos = models.IntegerField()
    traffic = models.DecimalField(max_digits=13, decimal_places=12)


class MER_NORM(models.Model):
    idData = models.AutoField(primary_key=True)
    date = models.DateField()
    CO = models.DecimalField(max_digits=13, decimal_places=12)
    NO = models.DecimalField(max_digits=13, decimal_places=12)
    NOX = models.DecimalField(max_digits=13, decimal_places=12)
    NO2 = models.DecimalField(max_digits=13, decimal_places=12)
    O3 = models.DecimalField(max_digits=13, decimal_places=12)
    PM10 = models.DecimalField(max_digits=13, decimal_places=12)
    PM25 = models.DecimalField(max_digits=13, decimal_places=12)
    RH = models.DecimalField(max_digits=3, decimal_places=2)
    SO2 = models.DecimalField(max_digits=13, decimal_places=12)
    TMP = models.DecimalField(max_digits=13, decimal_places=12)
    WDR = models.DecimalField(max_digits=13, decimal_places=12)
    WSP = models.DecimalField(max_digits=13, decimal_places=12)
    year = models.IntegerField()
    day = models.IntegerField()
    hora = models.IntegerField()
    minutos = models.IntegerField()
    traffic = models.DecimalField(max_digits=13, decimal_places=12)

class UIZ_NORM(models.Model):
    idData = models.AutoField(primary_key=True)
    date = models.DateField()
    CO = models.DecimalField(max_digits=13, decimal_places=12)
    NO = models.DecimalField(max_digits=13, decimal_places=12)
    NOX = models.DecimalField(max_digits=13, decimal_places=12)
    NO2 = models.DecimalField(max_digits=13, decimal_places=12)
    O3 = models.DecimalField(max_digits=13, decimal_places=12)
    PM10 = models.DecimalField(max_digits=13, decimal_places=12)
    PM25 = models.DecimalField(max_digits=13, decimal_places=12)
    RH = models.DecimalField(max_digits=3, decimal_places=2)
    SO2 = models.DecimalField(max_digits=13, decimal_places=12)
    TMP = models.DecimalField(max_digits=13, decimal_places=12)
    WDR = models.DecimalField(max_digits=13, decimal_places=12)
    WSP = models.DecimalField(max_digits=13, decimal_places=12)
    year = models.IntegerField()
    day = models.IntegerField()
    hora = models.IntegerField()
    minutos = models.IntegerField()
    traffic = models.DecimalField(max_digits=13, decimal_places=12)