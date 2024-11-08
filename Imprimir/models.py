from django.db import models

class Maquina(models.Model):
    nome = models.CharField(db_column='NAME', max_length=255)

    class Meta:
        db_table = 'INVENTORY'
        managed = False