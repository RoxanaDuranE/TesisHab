# Generated by Django 3.2.5 on 2024-04-05 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ConfiguracionApp', '0002_initial'),
        ('SolicitudesApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresupuestoDatoGen',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Fecha', models.DateField()),
                ('MejoraReal', models.CharField(max_length=200)),
                ('DiasEstiCon', models.CharField(max_length=10)),
                ('IdSolicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SolicitudesApp.solicitud')),
            ],
            options={
                'verbose_name': 'PresupuestoDatoGen',
                'verbose_name_plural': 'PresupuestoDatoGens',
                'db_table': 'PresupuestoDatoGen',
            },
        ),
        migrations.CreateModel(
            name='PresupuestoOtro',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Descripcion', models.CharField(max_length=100)),
                ('Unidad', models.CharField(max_length=10)),
                ('PrecioUnit', models.DecimalField(decimal_places=2, max_digits=15)),
                ('Cantidad', models.DecimalField(decimal_places=2, max_digits=15)),
                ('SubTota', models.DecimalField(decimal_places=2, max_digits=20)),
                ('IdPresupuestoDatoGen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PresupuestoApp.presupuestodatogen')),
            ],
            options={
                'verbose_name': 'PresupuestoOtro',
                'verbose_name_plural': 'PresupuestoOtros',
                'db_table': 'PresupuestoOtro',
            },
        ),
        migrations.CreateModel(
            name='PresupuestoMate',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('PrecioUnit', models.DecimalField(decimal_places=2, max_digits=15)),
                ('Cantidad', models.DecimalField(decimal_places=2, max_digits=15)),
                ('SubTota', models.DecimalField(decimal_places=2, max_digits=20)),
                ('IdMateriales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ConfiguracionApp.materiales')),
                ('IdPresupuestoDatoGen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PresupuestoApp.presupuestodatogen')),
            ],
            options={
                'verbose_name': 'PresupuestoMate',
                'verbose_name_plural': 'PresupuestoMates',
                'db_table': 'PresupuestoMate',
            },
        ),
        migrations.CreateModel(
            name='PresupuestoManoObr',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Descripcion', models.CharField(max_length=100)),
                ('Unidad', models.CharField(max_length=10)),
                ('PrecioUnit', models.DecimalField(decimal_places=2, max_digits=15)),
                ('Cantidad', models.DecimalField(decimal_places=2, max_digits=15)),
                ('SubTota', models.DecimalField(decimal_places=2, max_digits=20)),
                ('IdPresupuestoDatoGen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PresupuestoApp.presupuestodatogen')),
            ],
            options={
                'verbose_name': 'PresupuestoManoObr',
                'verbose_name_plural': 'PresupuestoManoObrs',
                'db_table': 'PresupuestoManoObr',
            },
        ),
        migrations.CreateModel(
            name='Presupuesto',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('SubTota', models.DecimalField(decimal_places=2, max_digits=15)),
                ('AsistenciaTecn', models.DecimalField(decimal_places=2, max_digits=15)),
                ('ComisionPorOto', models.DecimalField(decimal_places=2, max_digits=15)),
                ('ConsultaBuroCre', models.DecimalField(decimal_places=2, max_digits=15)),
                ('CancelarSaldPen', models.DecimalField(decimal_places=2, max_digits=15)),
                ('PrimeraCuot', models.DecimalField(decimal_places=2, max_digits=15)),
                ('Total', models.DecimalField(decimal_places=2, max_digits=20)),
                ('Notas', models.CharField(max_length=500)),
                ('IdPresupuestoDatoGen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PresupuestoApp.presupuestodatogen')),
            ],
            options={
                'verbose_name': 'Presupuesto',
                'verbose_name_plural': 'Presupuestos',
                'db_table': 'Presupuesto',
            },
        ),
    ]
