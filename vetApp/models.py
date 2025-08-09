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
        return self.nombre
    
    
class Doctor(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    numero_licencia = models.CharField(max_length=50, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Dr. {self.nombre} - {self.especialidad}"
    
    
class Cita(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='citas')
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='citas')
    fecha = models.DateTimeField(verbose_name="Fecha y hora de la cita")
    motivo = models.CharField(max_length=255, verbose_name="Motivo de la cita")
    notas = models.TextField(blank=True, null=True, verbose_name="Notas adicionales")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name="Estado de la cita")


    def __str__(self):
        return f"Cita de {self.paciente.nombre} con {self.doctor.nombre if self.doctor else 'Sin asignar'} el {self.fecha.strftime('%d/%m/%Y %H:%M')}"