from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_maquinas, name='lista_maquinas'),
    path('visualizar-selecionadas/', views.visualizar_maquinas_selecionadas, name='visualizar_maquinas_selecionadas'),
    path('remover-maquina/<str:nome>/', views.remover_maquina, name='remover_maquina'),
    path('imprimir-etiqueta/customizada/', views.imprimir_etiqueta_customizada, name='imprimir_etiqueta_customizada'),
    path('imprimir-etiqueta/visualizar/<str:nome>/', views.visualizar_etiqueta, name='visualizar_etiqueta'),
    path('imprimir-etiqueta/<str:nome>/', views.imprimir_etiqueta, name='imprimir_etiqueta'),
    path('maquinas/', views.lista_maquinas, name='lista_maquinas'),
]