from .auth_utils import get_current_employee


def employee(request):
    return {'employee': get_current_employee(request)}
