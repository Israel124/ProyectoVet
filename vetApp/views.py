from datetime import datetime, timedelta, time

from django.shortcuts import redirect, render

from vetApp.forms import LoginForm

# Create your views here.

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