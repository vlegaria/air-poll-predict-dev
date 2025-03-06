from django.urls import path

from . import views

urlpatterns = [
    path("prediccion/", views.prediccion.as_view(), name="prediccion"),
    path("ultimaspredic/", views.ultimaspredicciones.as_view(), name="ultimaspredic")    
]