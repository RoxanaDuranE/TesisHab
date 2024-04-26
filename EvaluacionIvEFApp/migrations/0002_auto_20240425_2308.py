# Generated by Django 3.2.5 on 2024-04-26 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EvaluacionIvEFApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capacidadpagofam',
            name='PorcentajeCuot',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='capacidadpagofam',
            name='PorcentajeDisp',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='capacidadpagofam',
            name='PorcentajeEnde',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='egresosfami',
            name='Afp',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='egresosfami',
            name='Alimentacion',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='egresosfami',
            name='Alquiler',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='egresosfami',
            name='Educacion',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='egresosfami',
            name='Imprevistos',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='egresosfami',
            name='OtrosDesc',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='egresosfami',
            name='PorcentajeHplhes',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='egresosfami',
            name='PorcentajePlan',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='egresosfami',
            name='PorcentajeVent',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='egresosfami',
            name='Recreacion',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='egresosfami',
            name='Salud',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='egresosfami',
            name='Servicios',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='egresosfami',
            name='Transporte',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ingresosfami',
            name='Familiar',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ingresosfami',
            name='OtrosIngr',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
