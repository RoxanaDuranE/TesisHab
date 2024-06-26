# Generated by Django 3.2.5 on 2024-04-05 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Nombres', models.CharField(max_length=50)),
                ('Apellidos', models.CharField(max_length=50)),
                ('Dui', models.CharField(max_length=12)),
                ('Telefono', models.CharField(max_length=10)),
                ('Nacionalidad', models.CharField(max_length=50)),
                ('FechaNaci', models.DateField()),
                ('Edad', models.IntegerField()),
                ('Salario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Direccion', models.CharField(max_length=100)),
                ('Correo', models.CharField(max_length=40)),
                ('Contrasena', models.CharField(max_length=500)),
                ('ContrasenaVeri', models.CharField(max_length=500)),
                ('Estado', models.CharField(max_length=10)),
                ('FechaRegi', models.DateField(auto_now_add=True)),
                ('EstadoSoli', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfils',
                'db_table': 'Perfil',
            },
        ),
        migrations.CreateModel(
            name='PerfilNoApl',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Nombres', models.CharField(max_length=50)),
                ('Apellidos', models.CharField(max_length=50)),
                ('Dui', models.CharField(max_length=12)),
                ('Telefono', models.CharField(max_length=10)),
                ('Nacionalidad', models.CharField(max_length=50)),
                ('Fecha', models.DateField()),
                ('Edad', models.IntegerField()),
                ('Salario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Direccion', models.CharField(max_length=100)),
                ('Observaciones', models.CharField(max_length=300, null=True)),
                ('FechaRegi', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'PerfilNoApl',
                'verbose_name_plural': 'PerfilNoApls',
                'db_table': 'PerfilNoApl',
            },
        ),
    ]
