# Generated by Django 3.2.5 on 2024-04-26 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SolicitudInscripcionSApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudinscseg',
            name='DesignoBene',
            field=models.CharField(max_length=28),
        ),
        migrations.AlterField(
            model_name='solicitudinscseg',
            name='Estatura',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='solicitudinscseg',
            name='MontoTotaAse',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='solicitudinscseg',
            name='MontosAsegAnt',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='solicitudinscseg',
            name='NuevoMontAse',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='solicitudinscseg',
            name='Peso',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='solicitudinscsegdefampdeffis',
            name='BebidasAlco',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='solicitudinscsegdefampdeffis',
            name='CuantosDia',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='solicitudinscsegdefampdeffis',
            name='FrecuenciaBebiAlc',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='solicitudinscsegdefampdeffis',
            name='FumaCigaPip',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='solicitudinscsegdefampdeffis',
            name='PracticaActiDep',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='solicitudinscsegdefampdeffis',
            name='SeguroDese',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='solicitudinscsegdefampdeffis',
            name='TieneDefoAmpDefFis',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='solicitudinscsegdefampdeffis',
            name='TratamientoMedi',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='solicitudinscsegpad',
            name='SituacionActu',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='solicitudinscsegpad',
            name='TratamientoReci',
            field=models.CharField(max_length=100),
        ),
    ]
