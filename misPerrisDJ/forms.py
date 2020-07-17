import re
from django import forms
from django.forms import ModelForm
from .models import Mascota, Busqueda, Persona, Adopcion


# Formulario de inicio de sesion.
class IniciarSesionForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(), label="Nombre de Usuario")
    password = forms.CharField(
        widget=forms.PasswordInput(), label="Contraseña")


# formulario de mantenedor de rescatados.
class nuevoRescatadoForm(ModelForm):
    class Meta:
        model = Mascota
        fields = ('nombre', 'raza', 'imagen', 'descripcion')


# Formulario de filtros de galeria de perritos.
class filtrarGaleriaForm(ModelForm):
    class Meta:
        model = Busqueda
        fields = ['estado']


# Formulario para el registro de postulantes.
class RegistrarPersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = ('nombre', 'apellido', 'rut', 'nacimiento', 'email',
                  'telefono', 'region', 'ciudad', 'vivienda')


# Formulario para el registro de experiencia de adopcion.
class registrarExperienciaForm(ModelForm):
    class Meta:
        model = Adopcion
        fields = ['descripcion']
