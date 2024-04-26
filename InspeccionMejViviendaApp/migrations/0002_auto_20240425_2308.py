# Generated by Django 3.2.5 on 2024-04-26 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InspeccionMejViviendaApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descripcionmejoinsmej',
            name='Descripcion',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='descripcionmejoinsmej',
            name='DiasEsti',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='factibilidadinsmej',
            name='Detalle',
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name='infraestructurainmuinsmej',
            name='Estado',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='infraestructurainmuinsmej',
            name='Existe',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='infraestructurainmuinsmej',
            name='TipoSist',
            field=models.CharField(max_length=75),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='Adultos',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='ExisteOtrViv',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='Hora',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='Inmueble',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='Latitud',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='Longitud',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='Ninos',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='ParentescoSoli',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='PersonaDisc',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='TelefonoPrim',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='TelefonoSegu',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='TerceraEdad',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='UsoActu',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='inspeccionmejo',
            name='UsoActuOtrViv',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='inspeccionmejoespserinfrie',
            name='Existe',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='planmejoinsmej',
            name='Descripcion',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='planmejoinsmej',
            name='Etapas',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='primerainspmej',
            name='MejoraReal',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='primerainspmej',
            name='NumeroInsp',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='riesgosinsmej',
            name='DistanciaLadeCer',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='riesgosinsmej',
            name='DistanciaRiosCer',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='riesgosinsmej',
            name='DistanciaTalu',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='riesgosinsmej',
            name='DistanciaTorrCer',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='viasacceinsmej',
            name='TipoVias',
            field=models.CharField(max_length=30),
        ),
    ]
