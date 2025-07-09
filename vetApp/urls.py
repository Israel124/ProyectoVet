from django.urls import path
from . import views

  # path('login/', views.login_view, name='login'),
  # path('logout/', views.logout_view, name='logout'),
  # path('register/', views.register, name='register'),

urlpatterns = [
  path('', views.home, name='home'),
  path('citas/', views.citas, name='citas'),
  path('register/', views.register, name='register'),
  path('login/', views.login_view, name='login'),
  path('cliente/', views.Clientes_view, name='cliente'),
  path('pacientes/', views.Paciente_view, name='pacientes'),
  path('reportes/', views.Reportes_view, name='reportes'),
]