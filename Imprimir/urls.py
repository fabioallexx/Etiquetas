from django.urls import path
from . import views

urlpatterns = [
    path('imprimir-etiqueta/visualizar/', views.visualizar_etiqueta, name='visualizar_etiqueta'),
    path('imprimir-etiqueta/', views.imprimir_etiqueta, name='imprimir_etiqueta'),
    path('maquinas/', views.lista_maquinas, name='lista_maquinas'),
]