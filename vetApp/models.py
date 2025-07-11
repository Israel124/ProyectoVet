from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Clientes(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    cedula = models.CharField(max_length=30, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE,verbose_name="Dueño de la mascota" )

    def __str__(self):
        return f"Nombre de la mascota: {self.nombre} - Especie: {self.especie} - Raza: {self.raza} - Dueño: {self.cliente.nombre}"