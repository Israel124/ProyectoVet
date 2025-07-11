from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class DueñoForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre completo")
    telefono = forms.CharField(max_length=20, label="Teléfono")
    email = forms.EmailField(label="Correo electrónico", required=False)
    direccion = forms.CharField(max_length=200, label="Dirección", required=False)
    cedula = forms.CharField(max_length=30, label="Cédula", required=False)
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", required=False, widget=forms.DateInput(attrs={'type': 'date'}))


class PacienteForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre de la mascota")
    especie = forms.CharField(max_length=50, label="Especie")
    raza = forms.CharField(max_length=50, label="Raza")
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    

class ReporteForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha")
    paciente = forms.CharField(max_length=100, label="Paciente")
    veterinario = forms.CharField(max_length=100, label="Veterinario", required=False)
    descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")
    diagnostico = forms.CharField(widget=forms.Textarea, label="Diagnóstico", required=False)
    tratamiento = forms.CharField(widget=forms.Textarea, label="Tratamiento", required=False)


class ClientesForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre completo")
    telefono = forms.CharField(max_length=20, label="Teléfono")
    email = forms.EmailField(label="Correo electrónico", required=False)
    direccion = forms.CharField(max_length=200, label="Dirección", required=False)
    cedula = forms.CharField(max_length=30, label="Cédula", required=False)
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", required=False, widget=forms.DateInput(attrs={'type': 'date'}))


class RegistroForm(forms.Form):
    username = forms.CharField(max_length=150, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    email = forms.EmailField(label="Correo electrónico")
    nombre = forms.CharField(max_length=100, label="Nombre completo")
    telefono = forms.CharField(max_length=20, label="Teléfono")
    direccion = forms.CharField(max_length=200, label="Dirección", required=False)
    cedula = forms.CharField(max_length=30, label="Cédula", required=False)
    # fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error('password2', "Las contraseñas no coinciden.")
        return cleaned_data
