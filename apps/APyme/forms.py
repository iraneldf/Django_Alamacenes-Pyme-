from crum import get_current_user
from django.forms import ModelForm, CharField, DecimalField, TextInput, IntegerField, NumberInput

from apps.APyme.models import *


class AlmacenForm(ModelForm):
    producto = CharField(max_length=100,
                         required=True,
                         widget=TextInput(
                             attrs={'class': 'form-control', 'placeholder': 'Entre el nombre de producto'}))
    cantidad = IntegerField(max_value=99999, required=True,
                            widget=NumberInput(
                                attrs={'class': 'form-control w-50', 'placeholder': 'Entre la cantidad'}))

    precio = DecimalField(required=True,
                          widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entre el precio'}))

    class Meta:
        model = Almacen
        fields = ['producto', 'precio', 'cantidad', 'unidad']

    def save(self, commit=True):
        prod = super().save(commit=False)
        print('el usuario es:', get_current_user())
        prod.user = get_current_user()
        if commit:
            prod.save()
        return prod


class AlmacenFormRoot(ModelForm):
    producto = CharField(max_length=100,
                         required=True,
                         widget=TextInput(
                             attrs={'class': 'form-control', 'placeholder': 'Entre el nombre de producto'}))
    cantidad = IntegerField(max_value=99999, required=True,
                            widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entre la cantidad'}))

    precio = DecimalField(required=True,
                          widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entre el precio'}))

    class Meta:
        model = Almacen
        fields = ['producto', 'precio', 'cantidad', 'unidad']


class ActAlmacenForm(ModelForm):
    producto = CharField(max_length=100,
                         required=True,
                         widget=TextInput(
                             attrs={'class': 'form-control', 'placeholder': 'Entre el nombre de producto'}))
    cantidad = IntegerField(required=True,
                            widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entre la cantidad'}))

    precio = DecimalField(required=True,
                          widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entre el precio'}))

    class Meta:
        model = Almacen
        fields = ['producto', 'precio', 'cantidad', 'unidad']


class BuscandoForm(ModelForm):
    producto = CharField(max_length=100,
                         required=True,
                         widget=TextInput(
                             attrs={'class': 'form-control',
                                    'placeholder': 'Entre el nombre de producto'}))
    cantidad = IntegerField(max_value=99999, required=False,
                            widget=NumberInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Entre la cantidad'}))

    precio = DecimalField(required=False, widget=NumberInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Entre el precio'}))

    class Meta:
        model = Buscando
        fields = ['producto', 'precio', 'cantidad', 'unidad']

    def save(self, commit=True):
        prod = super().save(commit=False)
        prod.user = get_current_user()
        if commit:
            prod.save()
        return prod


class BuscandoFormRoot(ModelForm):
    producto = CharField(max_length=100,
                         required=True,
                         widget=TextInput(
                             attrs={'class': 'form-control',
                                    'placeholder': 'Entre el nombre de producto'}))
    cantidad = IntegerField(max_value=99999, required=False,
                            widget=NumberInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Entre la cantidad'}))

    precio = DecimalField(required=False, widget=NumberInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Entre el precio'}))

    class Meta:
        model = Buscando
        fields = ['producto', 'precio', 'cantidad', 'unidad']


class TelefonoForm(ModelForm):
    class Meta:
        model = Telefonos
        fields = ['telefono']

    def save(self, commit=True):
        prod = super().save(commit=False)
        prod.perfil = get_current_user()
        if commit:
            prod.save()
        return prod


class TelefonoFormRoot(ModelForm):
    class Meta:
        model = Telefonos
        fields = ['telefono']


class WhatsappForm(ModelForm):
    class Meta:
        model = Whastapp
        fields = ['telefono']

    def save(self, commit=True):
        prod = super().save(commit=False)
        prod.perfil = get_current_user()
        if commit:
            prod.save()
        return prod


class WhatsappFormRoot(ModelForm):
    class Meta:
        model = Whastapp
        fields = ['telefono']


class SociosForm(ModelForm):
    class Meta:
        model = Socios
        fields = ['nombre']

    def save(self, commit=True):
        prod = super().save(commit=False)
        prod.perfil = get_current_user()
        if commit:
            prod.save()
        return prod


class SociosFormRoot(ModelForm):
    class Meta:
        model = Socios
        fields = ['nombre']


class DomiciliosForm(ModelForm):
    class Meta:
        model = Domicilios
        fields = ['domicilio']

    def save(self, commit=True):
        prod = super().save(commit=False)
        prod.perfil = get_current_user()
        if commit:
            prod.save()
        return prod


class DomiciliosFormRoot(ModelForm):
    class Meta:
        model = Domicilios
        fields = ['domicilio']


class CorreoForm(ModelForm):
    class Meta:
        model = Emails
        fields = ['email']

    def save(self, commit=True):
        prod = super().save(commit=False)
        prod.perfil = get_current_user()
        if commit:
            prod.save()
        return prod


class CorreoFormRoot(ModelForm):
    class Meta:
        model = Emails
        fields = ['email']


class SitiosForm(ModelForm):
    class Meta:
        model = Sitios
        fields = ['sitio']

    def save(self, commit=True):
        prod = super().save(commit=False)
        prod.perfil = get_current_user()
        if commit:
            prod.save()
        return prod


class SitiosFormRoot(ModelForm):
    class Meta:
        model = Sitios
        fields = ['sitio']
