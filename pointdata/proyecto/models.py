from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class AdministradorUsuario(BaseUserManager):
    def create_superuser(self, correo, nombre, password):
        if not correo:
            raise ValueError('El usuario debe tener un correo')

        correo_normalizado = self.normalize_email(correo)

        admin = self.model(correo=correo_normalizado, nombre=nombre)
        admin.set_password(password)

        admin.is_superuser = True
        admin.is_staff = True

        admin.save()


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    correo = models.EmailField(unique=True, null=False)
    nombre = models.TextField()
    apellido = models.TextField()
    fechaCreacion = models.DateField(
        auto_now_add=True, db_column='fecha_creacion')
    fechaActualizacion = models.DateTimeField(
        auto_now=True, db_column='fecha_actualizacion')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    objects= AdministradorUsuario()

    class Meta:
        db_table = 'usuarios'


class Tienda(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField(null=False)
    direccion = models.TextField(null=False)
    tipo = models.TextField(
        choices=(('BODEGA', 'BODEGA'), ('MERCADO', 'MERCADO')))
    fechaCreacion = models.DateTimeField(
        auto_now_add=True, db_column='fecha_creacion')
    fechaActualizacion = models.DateTimeField(
        auto_now=True, db_column='fecha_actualizacion')

    class Meta:
        db_table = 'tiendas'


class Relevo(models.Model):
    id = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='imagenes_relevos/', null=True)
    fechaCreacion = models.DateTimeField(
        auto_now_add=True, db_column='fecha_creacion')
    implementado = models.TextField(choices=(
        ('MERCADERISMO', 'MERCADERISMO'), ('SIN MERCADERISMO', 'SIN MERCADERISMO')))
    estado = models.TextField(choices=(
        ('EFECTIVO', 'EFECTIVO'), ('NO DESEA', 'NO DESEA'), ('CERRADO', 'CERRADO')))

    usuario = models.ForeignKey(
        to=Usuario, on_delete=models.PROTECT, db_column='usuario_id')
    tienda = models.ForeignKey(
        to=Tienda, on_delete=models.PROTECT, db_column='tienda_id')

    class Meta:
        db_table = 'relevos'
