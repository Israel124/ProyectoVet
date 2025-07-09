from datetime import datetime, timedelta, time
from django.shortcuts import redirect, render
from vetApp.forms import LoginForm
from vetApp.forms import LoginForm, ClientesForm, PacienteForm, ReporteForm
from vetApp.models import Paciente, Clientes
from django.views.generic import TemplateView
from django.views import View
from django import forms
from .forms import ClientesForm
from .models import Clientes


def home(request):
  
  contexto = {}
  
  return render(request, 'Home/home.html', contexto)

def citas(request):
  
    contexto = {}
    
    return render(request, 'Home/GestionCitas.html', contexto)


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
    return redirect('citas')
  else:
    form = LoginForm()
  response = render(request, 'login/login.html', {
        'form': form,
        # 'debug': settings.DEBUG
    })
  
  
  return response


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

# Vista de reportes
def Reportes_view(request):
    if request.method == 'POST':
        return redirect('Reportes')
    else:
        form = ReporteForm()
    
    return render(request, 'reportes/Reportes.html', {
        'form': form
    })

def Clientes_view(request):
    if request.method == 'POST':
        form = ClientesForm(request.POST)
        if form.is_valid():
            Clientes.objects.create(**form.cleaned_data)
            return redirect('cliente')
    else:
        form = ClientesForm()
    return render(request, 'Clientes/Clientes.html', {'form': form})
