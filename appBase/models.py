from django.db import models

class clsUsuarios(models.Model):
    ACTIVO = [
        ('ACTIVO', 'ACTIVO'),('INACTIVO', 'INACTIVO')
    ]
    idusuario = models.CharField(primary_key=True, max_length=25,verbose_name='Identificacion')
    nombre = models.CharField(max_length=255, verbose_name='Nombre')
    cargo = models.CharField(max_length=50, verbose_name='Cargo')
    contrasena = models.CharField(max_length=255, verbose_name='Contraseña')
    correo = models.CharField(max_length=255, blank=False, null=False, verbose_name='Correo')
    activo = models.CharField(max_length=25,choices=ACTIVO, blank=True, null=True, verbose_name='Activo')
    token = models.CharField(max_length=25, blank=True, null=True, verbose_name='Token')
    cambiocontrasena = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'tblusuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self) -> str:
        return f'{self.idusuario}'
