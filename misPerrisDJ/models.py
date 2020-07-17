import os
import datetime

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings
from PIL import Image


class Mascota(models.Model):
    # opciones de tipos de mascotas.
    tipos = (('', 'Seleccione un estado.'), ('r', 'Rescatado'),
             ('a', 'Adoptado'), ('d', 'Disponible'))

    # Atributos de la clase.
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25)
    raza = models.CharField(max_length=30)
    estado = models.CharField(max_length=1, choices=tipos, default='r')
    descripcion = models.TextField(max_length=100)
    imagen = models.ImageField(upload_to='rescatados')

    # Metodo str de la clase.
    def __str__(self):
        return self.nombre + " " + self.raza

    # Ordenando alfabeticamente.
    class meta:
        ordering = ['nombre']


# Cargar la imagen con pillow.
def cargarImagen(instance, **kwargs):
    miImagen = Image.open(instance.imagen)
    miImagen.save(os.path.join(settings.MEDIA_ROOT, instance.imagen.name))


# Quitar imagen relacionada a la mascota eliminada.
def eliminarImagen(instance, **kwargs):
    instance.imagen.delete(False)


# Tareas de post grabacion.
post_save.connect(cargarImagen, Mascota)

# Tareas de post eliminacion.
post_delete.connect(eliminarImagen, Mascota)


# Modelo para realizar las busquedas en la galeria.
class Busqueda(models.Model):
    # opciones de tipos de mascotas.
    tipos = (('r', 'Rescatado'), ('a', 'Adoptado'), ('d', 'Disponible'))

    # Atributos de la clase.
    estado = models.CharField(max_length=1, choices=tipos, default='r')

    # Metodo str de la clase.
    def __str__(self):
        return self.estado


# Modelo para las personas adoptantes.
class Persona(models.Model):

    # ciudades para seleccionar.
    ciudades = (('', 'Seleccione una ciudad'), ('santiago', 'Santiago'),
                ('maipo', 'Isla de Maipo'), ('valparaiso', 'Valparaiso'),
                ('vina', 'Viña del Mar'), ('calera', 'Calera'), ('rancagua',
                                                                 'Rancagua'),
                ('san-fernando', 'San Fernando'), ('pichilemu', 'Pichilemu'),
                ('talca', 'Talca'), ('linares', 'Linares'), ('parral',
                                                             'Parral'))

    # Regiones para seleccionar
    regiones = (('', 'Seleccione una región'),
                ('santiago', 'Región Metropolitana'), ('valparaiso',
                                                       'Región de Valparaiso'),
                ('rancagua', "Región del Libertador Bernardo O'Higgins"),
                ('maule', 'Región del Maule'))

    # tipos de viviendas.
    viviendas = (('', 'Seleccione un tipo de vivienda'),
                 ('casa-patio-grande',
                  'Casa con patio grande'), ('casa-patio-pequeño',
                                             'Casa con patio pequeño'),
                 ('casa-sin-patio', 'Casa sin patio'), ('departamento',
                                                        'Departamento'))

    # Atributos de la clase.
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=25,
        verbose_name='Nombre',
        validators=[
            RegexValidator(r'^([A-Za-zÑñ\-]{3,})[\s]{0,1}([A-Za-zÑñ\-]{0,})$')
        ])
    apellido = models.CharField(
        max_length=30,
        verbose_name='Apellidos',
        validators=[
            RegexValidator(r'^([A-Za-zÑñ\-]{3,})[\s]{0,1}([A-Za-zÑñ\-]{0,})$')
        ])
    rut = models.CharField(
        max_length=10,
        unique=True,
        help_text='(ej: 12345678-9)',
        verbose_name='Rut',
        validators=[RegexValidator(r'^([0-9]{6,8}-[0-9Kk])$')])
    nacimiento = models.DateField(
        default=datetime.date.today,
        help_text='Formato: dd/mm/aaaa',
        verbose_name='Fec.Nacimiento')
    email = models.EmailField(validators=[
        RegexValidator(r'^[+a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$')
    ])
    telefono = models.CharField(
        max_length=15, null=True, blank=True, verbose_name='Teléfono')
    region = models.CharField(
        max_length=15, choices=regiones, default='', verbose_name='Región')
    ciudad = models.CharField(
        max_length=50, choices=ciudades, default='', verbose_name='Ciudad')
    vivienda = models.CharField(
        max_length=50, choices=viviendas, default='', verbose_name='Vivienda')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # Metodo str de l a clase.
    def __str__(self):
        return self.nombre

    # Ordenando alfabeticamente.
    class meta:
        ordering = ['apellido']


# Clase de relacion de una adopcion.
class Adopcion(models.Model):

    # Atributos de la clase.
    idPersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    idMascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=100, null=True, blank=True, default='')