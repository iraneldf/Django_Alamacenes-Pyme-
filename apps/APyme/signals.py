from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete

User = get_user_model()
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=Almacen)
def update_Almacen(sender, instance, created, **kwargs):
    if not created:
        if alarmas_almacenes.objects.all().filter(almacen=instance):
            alarmas_almacenes.objects.all().filter(almacen=instance).delete()


@receiver(post_save, sender=Buscando)
def update_Buscando(sender, instance, created, **kwargs):
    if not created:
        if alarmas_almacenes.objects.all().filter(buscando=instance):
            alarmas_almacenes.objects.all().filter(buscando=instance).delete()


@receiver(post_delete, sender=alarmas_almacenes)
def update_Buscando(sender, instance, **kwargs):
    if instance.alarma.almacenes.count() is 0:
        Alarmas.objects.get(id=instance.alarma.id).delete()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()
