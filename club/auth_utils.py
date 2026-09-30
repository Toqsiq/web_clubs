from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import Employee


# Роли из CHECK-ограничения БД:
#   main_admin  → club_id IS NULL
#   club_admin  → club_id IS NOT NULL
ROLE_ADMIN = 'main_admin'      # главный админ (тарифы, услуги, менеджеры)
ROLE_MANAGER = 'club_admin'    # админ клуба / менеджер (ПК, клиенты, сессии)

ADMIN_SECTIONS = {'tariffs', 'services', 'employees'}
MANAGER_SECTIONS = {'computers', 'clients', 'sessions'}


def get_current_employee(request):
    """Возвращает текущего сотрудника из сессии или None."""
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return None
    try:
        return Employee.objects.get(pk=employee_id, is_active=True)
    except Employee.DoesNotExist:
        request.session.flush()
        return None


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not get_current_employee(request):
            messages.warning(request, 'Войдите в систему, чтобы продолжить.')
            return redirect('club:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            employee = get_current_employee(request)
            if not employee:
                messages.warning(request, 'Войдите в систему, чтобы продолжить.')
                return redirect('club:login')
            if employee.role not in roles:
                messages.error(request, 'Недостаточно прав для этого действия.')
                return redirect('club:home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def can_access_section(employee, section):
    if not employee:
        return False
    if employee.role == ROLE_ADMIN:
        return section in ADMIN_SECTIONS or section == 'home'
    if employee.role == ROLE_MANAGER:
        return section in MANAGER_SECTIONS or section == 'home'
    return False


def role_display(role):
    """Человекочитаемое название роли."""
    return {
        'main_admin': 'Admin',
        'club_admin': 'Manager',
    }.get(role, role)
