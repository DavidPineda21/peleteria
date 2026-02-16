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


class clsVentas(models.Model):
    idventa = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    idusuario = models.ForeignKey('appBase.clsUsuarios', models.DO_NOTHING, db_column='idusuario', verbose_name='Usuario')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        managed = False
        db_table = 'tblventas'

    def __str__(self):
        return f"Venta #{self.id}"


class clsDetalleVenta(models.Model):
    iddetalle = models.AutoField(primary_key=True)
    idventa = models.ForeignKey(clsVentas, on_delete=models.CASCADE, db_column='idventa', related_name='detalles')
    idproducto = models.ForeignKey(clsProductos, on_delete=models.PROTECT,db_column='idproducto')
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'tbldetalleventa'

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
