# Generated by Django 3.2.5 on 2024-04-26 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClienteApp', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='Contrasena',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='ContrasenaVeri',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='Correo',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='Direccion',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='Nacionalidad',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='Telefono',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='perfilnoapl',
            name='Direccion',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='perfilnoapl',
            name='Nacionalidad',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='perfilnoapl',
            name='Telefono',
            field=models.CharField(max_length=9),
        ),
    ]