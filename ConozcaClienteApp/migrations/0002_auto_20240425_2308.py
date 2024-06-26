# Generated by Django 3.2.5 on 2024-04-26 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ConozcaClienteApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clienteactieco',
            name='CargoDese',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='clienteactieco',
            name='LugarTrab',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='clienteactieco',
            name='TiempoLabo',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='clienteactieco',
            name='TipoActi',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='clientedatogen',
            name='ConocidoComo',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='clientedatogen',
            name='CorreoElec',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='clientedatogen',
            name='DireccionDomi',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='clientedatogen',
            name='EstatusProp',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='clientedatogen',
            name='Nacionalidad',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='clientedatogen',
            name='NombreCony',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='clientedatogen',
            name='NombreConzCli',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='clientedatogen',
            name='NumeroDocu',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='clientedatogen',
            name='TelefonoCelu',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='clientedatogen',
            name='TelefonoFijo',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='clientedatoneg',
            name='DireccionNego',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='clientedatoneg',
            name='NombreNego',
            field=models.CharField(max_length=75),
        ),
        migrations.AlterField(
            model_name='clientedeclcli',
            name='ClasificacionCred',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='clientedeclcli',
            name='CuotaDeclCli',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='clientedeclcli',
            name='MontoDeclCli',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='clientedeclcli',
            name='ProcedenciaPagoAdi',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='clientedeclcli',
            name='RealizarPagoAdi',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='clienteparausoexc',
            name='CodigoEmpl',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='clienteparausoexc',
            name='ValideFirmNomFot',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='clienteparausoexc',
            name='VerificadoPor',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='clienteparausoexc',
            name='VerifiqueDire',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='clientepeps',
            name='Grado',
            field=models.CharField(max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='clientepeps',
            name='NombrePeps',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='clientepeps',
            name='PuestoDese',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='clientepeps',
            name='RelacionPeps',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='clientepeps',
            name='UstedPeps',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='clienteperftra',
            name='EspecificarOtroPer',
            field=models.CharField(max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name='clienteperftra',
            name='Prestamos',
            field=models.CharField(max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name='clientepersben',
            name='BeneficiarioPeps',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='clientepersben',
            name='DireccionPerm',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='clientepersben',
            name='NoApli',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='clientepersben',
            name='NombreComp',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='clientepersben',
            name='TipoDocuPers',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='clientereciremfam',
            name='Monto',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='clientereciremfam',
            name='NombreRemi',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='clientereciremfam',
            name='Parentesco',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='clientereciremfam',
            name='RecibeReme',
            field=models.CharField(max_length=3),
        ),
    ]
