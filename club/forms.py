from django import forms
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from .models import Tariff, Service, Client, Computer, Session, Employee, Club


class LoginForm(forms.Form):
    login = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логин', 'autofocus': True}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}),
    )

    def clean(self):
        cleaned = super().clean()
        login = cleaned.get('login')
        password = cleaned.get('password')
        if not login or not password:
            return cleaned
        try:
            employee = Employee.objects.get(login=login, is_active=True)
        except Employee.DoesNotExist:
            raise forms.ValidationError('Неверный логин или пароль.')
        valid = check_password(password, employee.password_hash)
        if not valid and employee.password_hash == password:
            valid = True
        if not valid:
            raise forms.ValidationError('Неверный логин или пароль.')
        cleaned['employee'] = employee
        return cleaned


class EmployeeForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Оставьте пустым, чтобы не менять'}),
        required=False,
    )

    class Meta:
        model = Employee
        fields = ['full_name', 'phone', 'login', 'club', 'role', 'is_active']
        labels = {
            'full_name': 'ФИО',
            'phone': 'Телефон',
            'login': 'Логин',
            'club': 'Клуб',
            'role': 'Роль',
            'is_active': 'Активен',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+7 (999) 123-45-67'}),
            'login': forms.TextInput(attrs={'class': 'form-input'}),
            'club': forms.Select(attrs={'class': 'form-input'}),
            'role': forms.Select(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [('club_admin', 'Manager')]
        self.fields['role'].initial = 'club_admin'
        self.fields['role'].widget = forms.Select(
            attrs={'class': 'form-input'},
            choices=[('club_admin', 'Manager')],
        )
        self.fields['club'].required = True
        self.fields['club'].empty_label = None
        # Пароль обязателен только при создании
        if not self.instance or not self.instance.pk:
            self.fields['password'].required = True
            self.fields['password'].widget.attrs['placeholder'] = 'Пароль'

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.role = 'club_admin'
        password = self.cleaned_data.get('password')
        if password:
            instance.password_hash = make_password(password)
        elif not instance.pk:
            raise forms.ValidationError('Укажите пароль для нового менеджера.')
        if not instance.club_id:
            raise forms.ValidationError('У менеджера должен быть указан клуб.')
        if commit:
            instance.save()
        return instance


class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = ['name', 'duration_minutes', 'price', 'description', 'is_active']
        labels = {
            'name': 'Название',
            'duration_minutes': 'Длительность (минуты)',
            'price': 'Цена (₽)',
            'description': 'Описание',
            'is_active': 'Активен',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': 0}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'description', 'is_active']
        labels = {
            'name': 'Название',
            'price': 'Цена (₽)',
            'description': 'Описание',
            'is_active': 'Активна',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': 0}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'phone', 'email', 'bonus_points', 'is_blocked']
        labels = {
            'full_name': 'ФИО',
            'phone': 'Телефон',
            'email': 'Email',
            'bonus_points': 'Бонусы',
            'is_blocked': 'Заблокирован',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+7 (999) 123-45-67'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'bonus_points': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'is_blocked': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk:
            instance.registration_date = timezone.now()
            if instance.bonus_points is None:
                instance.bonus_points = 0
        if commit:
            instance.save()
        return instance


class ComputerForm(forms.ModelForm):
    class Meta:
        model = Computer
        fields = [
            'computer_number', 'zone', 'status',
            'cpu', 'gpu', 'ram_gb', 'storage_gb', 'monitor', 'is_active'
        ]
        labels = {
            'computer_number': 'Номер ПК',
            'zone': 'Зона',
            'status': 'Статус',
            'cpu': 'Процессор',
            'gpu': 'Видеокарта',
            'ram_gb': 'ОЗУ (ГБ)',
            'storage_gb': 'Накопитель (ГБ)',
            'monitor': 'Монитор',
            'is_active': 'Активен',
        }
        widgets = {
            'computer_number': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'zone': forms.Select(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'cpu': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Intel Core i7-12700K'}),
            'gpu': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'NVIDIA RTX 4070'}),
            'ram_gb': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'storage_gb': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'monitor': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '27" 144Hz'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = [
            'client', 'computer', 'tariff',
            'start_time', 'end_time', 'status',
            'total_cost', 'payment_method', 'payment_status', 'paid_at'
        ]
        labels = {
            'client': 'Клиент',
            'computer': 'Компьютер',
            'tariff': 'Тариф',
            'start_time': 'Начало',
            'end_time': 'Окончание',
            'status': 'Статус',
            'total_cost': 'Стоимость (₽)',
            'payment_method': 'Способ оплаты',
            'payment_status': 'Статус оплаты',
            'paid_at': 'Дата оплаты',
        }
        widgets = {
            'client': forms.Select(attrs={'class': 'form-input'}),
            'computer': forms.Select(attrs={'class': 'form-input'}),
            'tariff': forms.Select(attrs={'class': 'form-input'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'total_cost': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': 0}),
            'payment_method': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Наличные / Карта'}),
            'payment_status': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Оплачено / Не оплачено'}),
            'paid_at': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']
        self.fields['end_time'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']
        self.fields['paid_at'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']
        self.fields['paid_at'].required = False
