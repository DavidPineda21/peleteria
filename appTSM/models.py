from django.db import models

class clsProductos(models.Model):
    idproducto = models.AutoField(primary_key=True)
    tipoproducto = models.CharField(max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    precio = models.FloatField(blank=True, null=True)
    precioxm = models.CharField(max_length=2, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblproductos'
