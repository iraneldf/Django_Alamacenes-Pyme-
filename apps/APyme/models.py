# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from AlacenenesPyme.settings import MEDIA_URL, STATIC_URL


class User(AbstractUser):
    email = models.EmailField('dirección de correo', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='img/logo', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_logo(self):
        if self.logo:
            return '{}{}'.format(MEDIA_URL, self.logo)
        else:
            return '{}{}'.format(STATIC_URL, 'img/user2-160x160.jpg')

    class Meta:
        verbose_name_plural = 'Perfil de empresa'
        verbose_name = 'Perfiles de empresas'


class Almacen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario_almacen', validators=[RegexValidator(
        regex=r'^[a-zA-Z]+$',
        message='El nombre debe contener solo letras'
    )])
    producto = models.CharField(max_length=100, verbose_name='producto')
    cantidad = models.PositiveIntegerField(verbose_name='cantidad')
    precio = models.DecimalField(verbose_name='precio', max_digits=8, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.producto


class Buscando(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario_buscando',
                             validators=[RegexValidator(
                                 regex=r'^[a-zA-Z]+$',
                                 message='El nombre debe contener solo letras'
                             )])
    producto = models.CharField(max_length=100, verbose_name='producto')
    cantidad = models.PositiveIntegerField(verbose_name='cantidad')
    precio = models.DecimalField(verbose_name='precio', max_digits=8, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.cantidad is None:
            self.cantidad = 0

        if self.precio is None:
            self.precio = 0

        super(Buscando, self).save()

    def __str__(self):
        return self.producto


class Telefonos(models.Model):
    perfil = models.ForeignKey(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, verbose_name='teléfono', validators=[RegexValidator(
        regex=r'^\d+$',
        message='El teléfono debe contener solo números'
    )])

    def __str__(self):
        return self.telefono

    class Meta:
        verbose_name_plural = 'Teléfonos'
        verbose_name = 'Teléfono'


class Whastapp(models.Model):
    perfil = models.ForeignKey(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, verbose_name='WhatsApp', validators=[RegexValidator(
        regex=r'^\d+$',
        message='El teléfono debe contener solo números'
    )])

    def __str__(self):
        return self.telefono

    class Meta:
        verbose_name_plural = 'Whastapps'
        verbose_name = 'Whastapp'


class Socios(models.Model):
    perfil = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=500, verbose_name='nombre', validators=[RegexValidator(
        regex=r'^[a-zA-Z]+$',
        message='El nombre debe contener solo letras'
    )])

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Nombres de los socios '
        verbose_name = 'Nombre del socio'


class Domicilios(models.Model):
    perfil = models.ForeignKey(User, on_delete=models.CASCADE)
    domicilio = models.CharField(max_length=200, verbose_name='domicilio')

    def __str__(self):
        return self.domicilio

    class Meta:
        verbose_name_plural = 'Domicilios sociales'
        verbose_name = 'Domicilio social'


class Emails(models.Model):
    perfil = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name='correo')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Emails'
        verbose_name = 'Email'


class Sitios(models.Model):
    perfil = models.ForeignKey(User, on_delete=models.CASCADE)
    sitio = models.CharField(max_length=100, verbose_name='sitio web', validators=[RegexValidator(
        regex=r'^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        message='Ingrese una URL válida de un sitio web (por ejemplo, "http://www.ejemplo.com")'
    )])

    def __str__(self):
        return self.sitio

    class Meta:
        verbose_name_plural = 'Sitios webs'
        verbose_name = 'Sitio web'


class Hash(models.Model):
    hash = models.CharField(max_length=10, verbose_name='hash', unique=True)


class Alarmas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='empresa_match')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='empresa_buscando')
    almacenes = models.ManyToManyField(Almacen, through='alarmas_almacenes')


class alarmas_almacenes(models.Model):
    alarma = models.ForeignKey(Alarmas, on_delete=models.CASCADE)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    buscando = models.ForeignKey(Buscando, on_delete=models.CASCADE)
