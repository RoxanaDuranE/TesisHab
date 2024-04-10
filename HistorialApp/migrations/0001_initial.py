# Generated by Django 3.2.5 on 2024-04-05 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('SolicitudesApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RangoHist',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Minimo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Maximo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Tipo', models.CharField(max_length=30)),
                ('Porcentaje', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'verbose_name': 'RangoHist',
                'verbose_name_plural': 'RangoHists',
                'db_table': 'RangoHist',
            },
        ),
        migrations.CreateModel(
            name='RegistroHist',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Puntaje', models.DecimalField(decimal_places=2, max_digits=5)),
                ('Fecha', models.DateField()),
                ('IdRango', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HistorialApp.rangohist')),
                ('IdSolicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SolicitudesApp.solicitud')),
            ],
            options={
                'verbose_name': 'RegistroHist',
                'verbose_name_plural': 'RegistroHists',
                'db_table': 'RegistroHist',
            },
        ),
    ]