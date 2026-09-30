from django.urls import path
from . import views

app_name = 'club'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Admin
    path('tariffs/', views.tariffs_list, name='tariffs'),
    path('tariffs/new/', views.tariff_create, name='tariff_create'),
    path('tariffs/<int:pk>/edit/', views.tariff_edit, name='tariff_edit'),
    path('services/', views.services_list, name='services'),
    path('services/new/', views.service_create, name='service_create'),
    path('services/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('employees/', views.employees_list, name='employees'),
    path('employees/new/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),

    # Manager
    path('computers/', views.computers_list, name='computers'),
    path('computers/new/', views.computer_create, name='computer_create'),
    path('computers/<int:pk>/edit/', views.computer_edit, name='computer_edit'),
    path('clients/', views.clients_list, name='clients'),
    path('clients/new/', views.client_create, name='client_create'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('sessions/', views.sessions_list, name='sessions'),
    path('sessions/new/', views.session_create, name='session_create'),
    path('sessions/<int:pk>/edit/', views.session_edit, name='session_edit'),
]
