# Generated by Django 2.1.2 on 2018-11-06 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misPerrisDJ', '0006_auto_20181105_0338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Busqueda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('r', 'Rescatado'), ('a', 'Adoptado'), ('d', 'Disponible')], default='r', max_length=1)),
            ],
        ),
        migrations.AlterField(
            model_name='mascota',
            name='imagen',
            field=models.ImageField(upload_to='rescatados'),
        ),
    ]
