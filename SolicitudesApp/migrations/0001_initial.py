# Generated by Django 3.2.5 on 2024-04-05 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ClienteApp', '0001_initial'),
        ('ConfiguracionApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('TipoObra', models.CharField(max_length=10)),
                ('Fecha', models.DateField()),
                ('Numero', models.CharField(max_length=12)),
                ('Comunidad', models.CharField(max_length=80)),
                ('Area', models.CharField(max_length=15)),
                ('Tipo', models.CharField(max_length=10)),
                ('TipoIngr', models.CharField(max_length=10, null=True)),
                ('Estado', models.CharField(max_length=15)),
                ('Observaciones', models.CharField(max_length=300, null=True)),
                ('EstadoSoli', models.IntegerField(null=True)),
                ('IdPerfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClienteApp.perfil')),
            ],
            options={
                'verbose_name': 'Solicitud',
                'verbose_name_plural': 'Solicitudes',
                'db_table': 'Solicitud',
            },
        ),
        migrations.CreateModel(
            name='Referencias',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=50)),
                ('Parentesco', models.CharField(max_length=15)),
                ('Domicilio', models.CharField(max_length=100)),
                ('Telefono', models.CharField(max_length=12)),
                ('EstadoSoli', models.IntegerField(null=True)),
                ('IdSolicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SolicitudesApp.solicitud')),
            ],
            options={
                'verbose_name': 'Referencias',
                'verbose_name_plural': 'Referencias',
                'db_table': 'Referencias',
            },
        ),
        migrations.CreateModel(
            name='Medio',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('RedesSoci', models.CharField(max_length=25)),
                ('Pvv', models.CharField(max_length=25)),
                ('Referenciado', models.CharField(max_length=25)),
                ('Perifoneo', models.CharField(max_length=25)),
                ('Radio', models.CharField(max_length=25)),
                ('FeriaVivi', models.CharField(max_length=25)),
                ('CampanaProm', models.CharField(max_length=25)),
                ('Otros', models.CharField(max_length=25)),
                ('Especifique', models.CharField(max_length=80)),
                ('EstadoSoli', models.IntegerField(null=True)),
                ('IdSolicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SolicitudesApp.solicitud')),
            ],
            options={
                'verbose_name': 'Medio',
                'verbose_name_plural': 'Medios',
                'db_table': 'Medio',
            },
        ),
        migrations.CreateModel(
            name='GrupoFami',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=50)),
                ('Edad', models.CharField(max_length=10)),
                ('Salario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Trabajo', models.CharField(max_length=50)),
                ('Parentesco', models.CharField(max_length=50)),
                ('EstadoSoli', models.IntegerField(null=True)),
                ('IdSolicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SolicitudesApp.solicitud')),
            ],
            options={
                'verbose_name': 'GrupoFami',
                'verbose_name_plural': 'GrupoFami',
                'db_table': 'GrupoFami',
            },
        ),
        migrations.CreateModel(
            name='ExperienciaCred',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Lugar', models.CharField(max_length=30, null=True)),
                ('Monto', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('FechaOtor', models.DateField(null=True)),
                ('Estado', models.CharField(max_length=12, null=True)),
                ('Cuota', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('PoseeExpe', models.BooleanField()),
                ('EstadoSoli', models.IntegerField(null=True)),
                ('IdSolicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SolicitudesApp.solicitud')),
            ],
            options={
                'verbose_name': 'ExperienciaCred',
                'verbose_name_plural': 'ExperienciaCreds',
                'db_table': 'ExperienciaCred',
            },
        ),
        migrations.CreateModel(
            name='Domicilio',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Direccion', models.CharField(max_length=100)),
                ('Referencia', models.CharField(max_length=50)),
                ('Telefono', models.CharField(max_length=15)),
                ('ResideDesd', models.CharField(max_length=50)),
                ('CondicionVivi', models.CharField(max_length=50)),
                ('LugarTrab', models.CharField(max_length=100)),
                ('ActividadMicr', models.CharField(max_length=50, null=True)),
                ('JefeInme', models.CharField(max_length=50, null=True)),
                ('TiempoEmprTieFun', models.CharField(max_length=50)),
                ('SalarioIngr', models.DecimalField(decimal_places=2, max_digits=10)),
                ('DireccionTrabMic', models.CharField(max_length=100)),
                ('TelefonoTrabMic', models.CharField(max_length=15)),
                ('Tipo', models.CharField(max_length=15)),
                ('EstadoSoli', models.IntegerField(null=True)),
                ('IdSolicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SolicitudesApp.solicitud')),
            ],
            options={
                'verbose_name': 'Domicilio',
                'verbose_name_plural': 'Domicilios',
                'db_table': 'Domicilio',
            },
        ),
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Plazo', models.CharField(max_length=50)),
                ('Cuota', models.DecimalField(decimal_places=2, max_digits=10)),
                ('FormaPago', models.CharField(max_length=15)),
                ('FechaPago', models.CharField(max_length=30)),
                ('EstadoSoli', models.IntegerField(null=True)),
                ('IdSolicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SolicitudesApp.solicitud')),
            ],
            options={
                'verbose_name': 'Detalle',
                'verbose_name_plural': 'Detalles',
                'db_table': 'Detalle',
            },
        ),
        migrations.CreateModel(
            name='DatosPersFia',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Tipo', models.CharField(max_length=12, null=True)),
                ('NombreFiad', models.CharField(max_length=50)),
                ('ApellidoFiad', models.CharField(max_length=50)),
                ('DuiFiad', models.CharField(max_length=12)),
                ('LugarDuiFia', models.CharField(max_length=30)),
                ('FechaDuiFia', models.DateField()),
                ('FechaNaciFia', models.DateField()),
                ('LugarNaciFia', models.CharField(max_length=30)),
                ('EdadFiad', models.IntegerField()),
                ('EstadoCiviFiad', models.CharField(max_length=30)),
                ('GeneroFiad', models.CharField(max_length=12)),
                ('EstadoFiad', models.IntegerField()),
                ('EstadoSoli', models.IntegerField(null=True)),
                ('IdOcupacionDUIFia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ocupacion_DUI_fiador', to='ConfiguracionApp.ocupacion')),
                ('IdOcupacionFia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ConfiguracionApp.ocupacion')),
                ('IdSolicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SolicitudesApp.solicitud')),
            ],
            options={
                'verbose_name': 'DatosPersFia',
                'verbose_name_plural': 'DatosPersFias',
                'db_table': 'DatosPersFia',
            },
        ),
        migrations.CreateModel(
            name='DatosPers',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('LugarDuiCli', models.CharField(max_length=100)),
                ('FechaDuiCli', models.DateField()),
                ('LugarNaciCli', models.CharField(max_length=100)),
                ('EstadoCiviCli', models.CharField(max_length=30)),
                ('GeneroClie', models.CharField(max_length=12)),
                ('EstadoClie', models.CharField(max_length=10)),
                ('EstadoSoli', models.IntegerField(null=True)),
                ('IdSolicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SolicitudesApp.solicitud')),
            ],
            options={
                'verbose_name': 'DatosPers',
                'verbose_name_plural': 'DatosPerss',
                'db_table': 'DatosPers',
            },
        ),
        migrations.CreateModel(
            name='DatosObra',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Dueno', models.CharField(max_length=50)),
                ('Parentesco', models.CharField(max_length=50)),
                ('DireccionExac', models.CharField(max_length=100)),
                ('DetalleAdic', models.CharField(max_length=80, null=True)),
                ('Presupuesto', models.DecimalField(decimal_places=2, max_digits=15)),
                ('EstadoSoli', models.IntegerField(null=True)),
                ('IdAlternativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ConfiguracionApp.alternativa')),
                ('IdModeloVivi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ConfiguracionApp.modelovivi')),
                ('IdSolicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SolicitudesApp.solicitud')),
            ],
            options={
                'verbose_name': 'DatosObra',
                'verbose_name_plural': 'DatosObras',
                'db_table': 'DatosObra',
            },
        ),
        migrations.CreateModel(
            name='Comentarios',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('ComentarioNeceVivMej', models.CharField(max_length=200)),
                ('ComentarioEvalEst', models.CharField(max_length=200)),
                ('ComentarioGaraOfr', models.CharField(max_length=200)),
                ('EstadoSoli', models.IntegerField(null=True)),
                ('IdSolicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SolicitudesApp.solicitud')),
            ],
            options={
                'verbose_name': 'Comentarios',
                'verbose_name_plural': 'Comentarios',
                'db_table': 'Comentarios',
            },
        ),
    ]
