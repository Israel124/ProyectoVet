# Generated by Django 5.2.3 on 2025-07-11 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vetApp', '0002_clientes_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientes',
            name='fecha_nacimiento',
        ),
    ]
