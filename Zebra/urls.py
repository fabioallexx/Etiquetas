from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('etiquetas/', include('Imprimir.urls')),
    path('', include('Imprimir.urls')),
]