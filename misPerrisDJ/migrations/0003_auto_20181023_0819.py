# Generated by Django 2.1.2 on 2018-10-23 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misPerrisDJ', '0002_mascota_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascota',
            name='estado',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='imagen',
            field=models.ImageField(upload_to='%Y/%m/%d/'),
        ),
    ]
