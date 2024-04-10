from django.db import models

# Create your models here.
class Departamento(models.Model):
    Id= models.AutoField(primary_key=True)
    NombreDepa=models.CharField(max_length=15)

    class Meta:
        verbose_name='Departamento'
        verbose_name_plural='Departamentos'
        db_table= 'Departamento'

    def __str__(self) :
        return self.NombreDepa
    
class Municipio(models.Model):
    Id= models.AutoField(primary_key=True)
    NombreMuni=models.CharField(max_length=22)
    IdDepartamento=models.ForeignKey(Departamento, on_delete=models.CASCADE)
    Estado=models.IntegerField()

    class Meta:
        verbose_name='Municipio'
        verbose_name_plural='Municipios'
        db_table= 'Municipio'

    def __str__(self) :
        return self.NombreMuni
    
class Distrito(models.Model):
    Id= models.AutoField(primary_key=True)
    Distrito=models.CharField(max_length=28)
    IdMunicipio=models.ForeignKey(Municipio, on_delete=models.CASCADE)
    Estado=models.IntegerField()
    
    class Meta:
        verbose_name='Distrito'
        verbose_name_plural='Distritos'
        db_table= 'Distrito'

    def __str__(self) :
        return self.Distrito