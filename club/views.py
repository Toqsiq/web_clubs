from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Tariff, Service, Computer, Client, Club, Session, Employee
from .forms import (
    TariffForm, ServiceForm, ClientForm, ComputerForm, SessionForm,
    LoginForm, EmployeeForm,
)
from .auth_utils import (
    get_current_employee, login_required, role_required,
    ROLE_ADMIN, ROLE_MANAGER,
)


def home(request):
    employee = get_current_employee(request)
    clubs = Club.objects.filter(is_active=True)
    tariffs_count = Tariff.objects.filter(is_active=True).count()
    services_count = Service.objects.filter(is_active=True).count()
    computers_count = Computer.objects.filter(is_active=True).count()

    return render(request, 'club/home.html', {
        'clubs': clubs,
        'tariffs_count': tariffs_count,
        'services_count': services_count,
        'computers_count': computers_count,
        'employee': employee,
    })


def login_view(request):
    if get_current_employee(request):
        return redirect('club:home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            request.session['employee_id'] = employee.id
            request.session['employee_role'] = employee.role
            request.session['employee_name'] = employee.full_name
            messages.success(request, f'Добро пожаловать, {employee.full_name}!')
            return redirect('club:home')
    else:
        form = LoginForm()
    return render(request, 'club/login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    messages.info(request, 'Вы вышли из системы.')
    return redirect('club:login')


# ─── Admin: тарифы ───────────────────────────────────────────

@role_required(ROLE_ADMIN)
def tariffs_list(request):
    tariffs = Tariff.objects.all().order_by('price')
    return render(request, 'club/tariffs.html', {
        'tariffs': tariffs,
        'employee': get_current_employee(request),
    })


@role_required(ROLE_ADMIN)
def tariff_create(request):
    if request.method == 'POST':
        form = TariffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тариф успешно добавлен!')
            return redirect('club:tariffs')
    else:
        form = TariffForm()
    return render(request, 'club/tariff_form.html', {
        'form': form,
        'title': 'Новый тариф',
        'employee': get_current_employee(request),
    })


@role_required(ROLE_ADMIN)
def tariff_edit(request, pk):
    tariff = get_object_or_404(Tariff, pk=pk)
    if request.method == 'POST':
        form = TariffForm(request.POST, instance=tariff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тариф обновлён!')
            return redirect('club:tariffs')
    else:
        form = TariffForm(instance=tariff)
    return render(request, 'club/tariff_form.html', {
        'form': form,
        'title': 'Редактировать тариф',
        'employee': get_current_employee(request),
    })


# ─── Admin: услуги ───────────────────────────────────────────

@role_required(ROLE_ADMIN)
def services_list(request):
    services = Service.objects.all().order_by('name')
    return render(request, 'club/services.html', {
        'services': services,
        'employee': get_current_employee(request),
    })


@role_required(ROLE_ADMIN)
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Услуга успешно добавлена!')
            return redirect('club:services')
    else:
        form = ServiceForm()
    return render(request, 'club/service_form.html', {
        'form': form,
        'title': 'Новая услуга',
        'employee': get_current_employee(request),
    })


@role_required(ROLE_ADMIN)
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Услуга обновлена!')
            return redirect('club:services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'club/service_form.html', {
        'form': form,
        'title': 'Редактировать услугу',
        'employee': get_current_employee(request),
    })


# ─── Admin: менеджеры ────────────────────────────────────────

@role_required(ROLE_ADMIN)
def employees_list(request):
    employees = Employee.objects.filter(role=ROLE_MANAGER).order_by('full_name')
    return render(request, 'club/employees.html', {
        'employees': employees,
        'employee': get_current_employee(request),
    })


@role_required(ROLE_ADMIN)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Менеджер успешно добавлен!')
            return redirect('club:employees')
    else:
        form = EmployeeForm()
    return render(request, 'club/employee_form.html', {
        'form': form,
        'title': 'Новый менеджер',
        'employee': get_current_employee(request),
    })


@role_required(ROLE_ADMIN)
def employee_edit(request, pk):
    emp = get_object_or_404(Employee, pk=pk, role=ROLE_MANAGER)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Менеджер обновлён!')
            return redirect('club:employees')
    else:
        form = EmployeeForm(instance=emp)
    return render(request, 'club/employee_form.html', {
        'form': form,
        'title': 'Редактировать менеджера',
        'employee': get_current_employee(request),
    })


# ─── Manager: компьютеры ─────────────────────────────────────

@role_required(ROLE_MANAGER)
def computers_list(request):
    computers = Computer.objects.select_related('zone', 'status').order_by('computer_number')
    return render(request, 'club/computers.html', {
        'computers': computers,
        'employee': get_current_employee(request),
    })


@role_required(ROLE_MANAGER)
def computer_create(request):
    if request.method == 'POST':
        form = ComputerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Компьютер успешно добавлен!')
            return redirect('club:computers')
    else:
        form = ComputerForm()
    return render(request, 'club/computer_form.html', {
        'form': form,
        'title': 'Новый компьютер',
        'employee': get_current_employee(request),
    })


@role_required(ROLE_MANAGER)
def computer_edit(request, pk):
    pc = get_object_or_404(Computer, pk=pk)
    if request.method == 'POST':
        form = ComputerForm(request.POST, instance=pc)
        if form.is_valid():
            form.save()
            messages.success(request, 'Компьютер обновлён!')
            return redirect('club:computers')
    else:
        form = ComputerForm(instance=pc)
    return render(request, 'club/computer_form.html', {
        'form': form,
        'title': 'Редактировать компьютер',
        'employee': get_current_employee(request),
    })


# ─── Manager: клиенты ────────────────────────────────────────

@role_required(ROLE_MANAGER)
def clients_list(request):
    clients = Client.objects.all().order_by('-registration_date')
    return render(request, 'club/clients.html', {
        'clients': clients,
        'employee': get_current_employee(request),
    })


@role_required(ROLE_MANAGER)
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Клиент добавлен!')
            return redirect('club:clients')
    else:
        form = ClientForm()
    return render(request, 'club/client_form.html', {
        'form': form,
        'title': 'Новый клиент',
        'employee': get_current_employee(request),
    })


@role_required(ROLE_MANAGER)
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Клиент обновлён!')
            return redirect('club:clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'club/client_form.html', {
        'form': form,
        'title': 'Редактировать клиента',
        'employee': get_current_employee(request),
    })


# ─── Manager: сессии ─────────────────────────────────────────

@role_required(ROLE_MANAGER)
def sessions_list(request):
    sessions = (
        Session.objects
        .select_related('client', 'computer', 'tariff', 'employee', 'status')
        .order_by('-start_time')
    )
    return render(request, 'club/sessions.html', {
        'sessions': sessions,
        'employee': get_current_employee(request),
    })


@role_required(ROLE_MANAGER)
def session_create(request):
    current = get_current_employee(request)
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.employee = current
            session.save()
            messages.success(request, 'Сессия успешно добавлена!')
            return redirect('club:sessions')
    else:
        form = SessionForm()
    return render(request, 'club/session_form.html', {
        'form': form,
        'title': 'Новая сессия',
        'employee': current,
    })


@role_required(ROLE_MANAGER)
def session_edit(request, pk):
    session = get_object_or_404(
        Session.objects.select_related('client', 'computer', 'tariff', 'status'),
        pk=pk,
    )
    current = get_current_employee(request)
    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сессия обновлена!')
            return redirect('club:sessions')
    else:
        form = SessionForm(instance=session)
    return render(request, 'club/session_form.html', {
        'form': form,
        'title': f'Редактировать сессию #{session.id}',
        'employee': current,
    })
