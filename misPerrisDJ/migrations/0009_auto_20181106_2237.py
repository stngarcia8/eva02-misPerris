# Generated by Django 2.1.2 on 2018-11-07 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misPerrisDJ', '0008_auto_20181106_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='region',
            field=models.CharField(choices=[('', 'Seleccione una región'), ('santiago', 'Región Metropolitana'), ('valparaiso', 'Región de Valparaiso'), ('rancagua', "Región del Libertador Bernardo O'Higgins")], default='', max_length=15),
        ),
        migrations.AddField(
            model_name='persona',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
