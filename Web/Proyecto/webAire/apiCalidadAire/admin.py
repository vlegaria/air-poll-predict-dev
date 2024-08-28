from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(estacionesCAME)
admin.site.register(EstatusCalidad)
admin.site.register(Contaminantes)
admin.site.register(Unidades)
admin.site.register(Prediccion)