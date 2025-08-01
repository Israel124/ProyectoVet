from datetime import datetime, timedelta, time
from django.shortcuts import redirect, render
from vetApp.forms import LoginForm
from vetApp.forms import LoginForm, ClientesForm, PacienteForm, ReporteForm
from vetApp.models import Paciente, Clientes
from django.views.generic import TemplateView
from django.views import View
from django import forms
from .forms import ClientesForm, RegistroForm
from .models import Clientes
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm #crea usuarios
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
  
  contexto = {}
  
  return render(request, 'Home/home.html', contexto)

@login_required
def citas(request):
  
    contexto = {}
    
    return render(request, 'Home/GestionCitas.html', contexto)


class VRegistro(View):
    def get(self, request):
        form = RegistroForm()
        return render(request, 'register/register.html', {'form': form})

    def post(self, request):
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['nombre']
            user = User.objects.create_user(
                username=username,
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            Clientes.objects.create(
                nombre=form.cleaned_data['nombre'],
                telefono=form.cleaned_data['telefono'],
                email=form.cleaned_data['email'],
                direccion=form.cleaned_data['direccion'],
                cedula=form.cleaned_data['cedula'],
                # fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                user=user
            )
            # return redirect('login')
            login(request, user )
            return redirect('home')
        
        return render(request, 'register/register.html', {'form': form})
  

def register(request):
    """Vista para registro de usuarios"""
    context = {
        'data': {},
        'errors': {},
        'especialidades':["dopakdoka", 'odaokdo'], #Doctor.ESPECIALIDADES,
        'yesterday': datetime.now().date() - timedelta(days=1),
        # 'debug': settings.DEBUG
    }
    
    
    
      
    return render(request, 'register/register.html', context)
  
  
  
def login_view(request):

  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      
      user = authenticate(username=username, password=password)
      if user is not None:
          login(request, user)
          
          
          
          # print(user.clientes.cedula)
          
          messages.success(request, '¡Bienvenido de vuelta!')
          
          if hasattr(user, 'doctor'):
              return redirect('citas')
              
          else: 
            print("entro aca")
            return redirect('home')
      else:
          messages.error(request, 'Usuario o contraseña incorrectos.')
  else: 
    form = LoginForm()
    return render(request, 'login/login.html', {
        'form': form,
        # 'debug': settings.DEBUG
    })
  # if request.method == 'POST':
  #   return redirect('citas')
  # else:
  #   form = LoginForm()
  # response = render(request, 'login/login.html', {
  #       'form': form,
  #       # 'debug': settings.DEBUG
  #   })
  
  
  # return response


def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('login')

@login_required
# Vista de pacientes
def Paciente_view(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            # Guardar los datos en la base de datos
            Paciente.objects.create(**form.cleaned_data)
            return redirect('Pacientes')
    else:
        form = PacienteForm()
    
    return render(request, 'paciente/Pacientes.html', {
        'form': form
    })
    
@login_required
# Vista de reportes
def Reportes_view(request):
    if request.method == 'POST':
        return redirect('Reportes')
    else:
        form = ReporteForm()
    
    return render(request, 'reportes/Reportes.html', {
        'form': form
    })
    
@login_required
def Clientes_view(request):
    if request.method == 'POST':
        form = ClientesForm(request.POST)
        if form.is_valid():
            Clientes.objects.create(**form.cleaned_data)
            return redirect('cliente')
    else:
        form = ClientesForm()
    return render(request, 'Clientes/Clientes.html', {'form': form})
