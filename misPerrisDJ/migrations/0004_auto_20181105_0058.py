# Generated by Django 2.1.2 on 2018-11-05 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misPerrisDJ', '0003_auto_20181023_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascota',
            name='estado',
            field=models.CharField(choices=[('', 'Seleccione un estado.'), ('r', 'Rescatado'), ('a', 'Adoptado'), ('d', 'Disponible')], default='', max_length=1),
        ),
    ]
