from crum import get_current_user
from django.forms import ModelForm, CharField, DecimalField, TextInput, IntegerField, NumberInput

from apps.APyme.models import *


class AlmacenForm(ModelForm):
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
        fields = ['producto', 'precio', 'cantidad']

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
        fields = ['producto', 'precio', 'cantidad']


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
        fields = ['producto', 'precio', 'cantidad']


class BuscandoForm(ModelForm):
    producto = CharField(max_length=100,
                         required=True,
                         widget=TextInput(
                             attrs={'class': 'form-control',
                                    'placeholder': 'Entre el nombre de qweqwe'}))
    cantidad = IntegerField(max_value=99999, required=False,
                            widget=NumberInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Entre la cantidad'}))

    precio = DecimalField(required=False, widget=NumberInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Entre el precio'}))

    class Meta:
        model = Buscando
        fields = ['producto', 'precio', 'cantidad']

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
                                    'placeholder': 'Entre el nombre de qweqwe'}))
    cantidad = IntegerField(max_value=99999, required=False,
                            widget=NumberInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Entre la cantidad'}))

    precio = DecimalField(required=False, widget=NumberInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Entre el precio'}))

    class Meta:
        model = Buscando
        fields = ['producto', 'precio', 'cantidad']


class TelefonoFormRoot(ModelForm):
    producto = CharField(max_length=100,
                         required=True,
                         widget=TextInput(
                             attrs={'class': 'form-control',
                                    'placeholder': 'Entre el nombre de qweqwe'}))
    cantidad = IntegerField(max_value=99999, required=False,
                            widget=NumberInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Entre la cantidad'}))

    precio = DecimalField(required=False, widget=NumberInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Entre el precio'}))

    class Meta:
        model = Buscando
        fields = ['producto', 'precio', 'cantidad']
