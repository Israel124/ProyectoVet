from datetime import datetime, timedelta, time
from django.shortcuts import redirect, render
from vetApp.forms import LoginForm
from vetApp.forms import LoginForm, ClientesForm, PacienteForm, ReporteForm, CitaForm
from vetApp.models import Paciente, Clientes
from django.views.generic import TemplateView
from django.views import View
from django import forms
from .forms import ClientesForm, RegistroForm
from .models import Clientes,Cita
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm #crea usuarios
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
def home(request):
  
  contexto = {}
  
  return render(request, 'Home/home.html', contexto)


import json
from django.core.serializers.json import DjangoJSONEncoder

@login_required
def citas(request):
    citas = Cita.objects.select_related('paciente', 'paciente__cliente', 'doctor').all()
    
    appointments_data = []
    for cita in citas:
        appointments_data.append({
            'id': cita.id,
            'petName': cita.paciente.nombre,
            'animalType': cita.paciente.especie.lower(),
            'breed': cita.paciente.raza,
            'age': (datetime.now().date() - cita.paciente.fecha_nacimiento).days // 365 if cita.paciente.fecha_nacimiento else 0,
            'date': cita.fecha.strftime('%Y-%m-%d'),
            'time': cita.fecha.strftime('%H:%M'),
            'description': cita.motivo,
            'status': cita.estado,
            'ownerName': cita.paciente.cliente.nombre,
            'phone': cita.paciente.cliente.telefono,
            'email': cita.paciente.cliente.email,
        })

    contexto = {
        'appointments_json': json.dumps(appointments_data, cls=DjangoJSONEncoder)
    }
    
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
            messages.success(request, '¡Bienvenido de vuelta!')
            return redirect('home')
            
            #   if hasattr(user, 'doctor'):
            #       return redirect('citas')
                
            #   else: 
            #     print("entro aca")
            #     return redirect('home')
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
    return render(request, 'GClientes/GestionClientes.html', {'form': form})


@login_required
def citas_cliente(request):
    # Obtener el cliente relacionado al usuario
    try:
        cliente = request.user.clientes
    except Clientes.DoesNotExist:
        messages.error(request, "No tienes perfil de cliente.")
        return redirect('home')

    # Mostrar solo las citas de los pacientes de este cliente
    pacientes = Paciente.objects.filter(cliente=cliente)
    citas = Cita.objects.filter(paciente__in=pacientes).order_by('-fecha')

    # Crear o editar cita
    if request.method == 'POST':
        if 'cita_id' in request.POST:
            cita = get_object_or_404(Cita, id=request.POST['cita_id'], paciente__cliente=cliente)
            form = CitaForm(request.POST, instance=cita)
        else:
            form = CitaForm(request.POST)
        if form.is_valid():
            nueva_cita = form.save(commit=False)
            # Solo permitir pacientes del cliente actual
            if nueva_cita.paciente.cliente != cliente:
                messages.error(request, "No puedes agendar citas para pacientes que no son tuyos.")
            else:
                nueva_cita.save()
                messages.success(request, "Cita guardada correctamente.")
                return redirect('citas_cliente')
    else:
        form = CitaForm()
        form.fields['paciente'].queryset = Paciente.objects.filter(cliente=cliente)

    return render(request, 'citas/citas_cliente.html', {
        'form': form,
        'citas': citas,
        'pacientes': pacientes,
    })

@login_required
def eliminar_cita(request, cita_id):
    try:
        cliente = request.user.clientes
    except Clientes.DoesNotExist:
        messages.error(request, "No tienes perfil de cliente.")
        return redirect('home')
    cita = get_object_or_404(Cita, id=cita_id, paciente__cliente=cliente)
    if request.method == 'POST':
        cita.delete()
        messages.success(request, "Cita eliminada correctamente.")
        return redirect('citas_cliente')
    return render(request, 'citas/confirmar_eliminar.html', {'cita': cita})