# Generated by Django 2.1.2 on 2018-11-07 22:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misPerrisDJ', '0015_auto_20181107_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='email',
            field=models.EmailField(max_length=254, validators=[django.core.validators.RegexValidator('^[+a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$')]),
        ),
    ]
