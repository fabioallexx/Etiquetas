from django.db import models

class Maquina(models.Model):
    nome = models.CharField(db_column="NAME", max_length=255)
    inventory_id = models.IntegerField(db_column="SEQUENCE", primary_key=True)

    class Meta:
        db_table = "[_SMDBA_].[_INVENTORY_]"
        managed = False