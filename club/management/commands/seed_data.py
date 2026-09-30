"""
Заполнение справочников.

Роли в БД (check_employee_club_role):
  main_admin  → club_id IS NULL
  club_admin  → club_id IS NOT NULL

Запуск:
    python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.hashers import make_password
from club.models import (
    Club, ComputerZone, ComputerStatus, SessionStatus, Employee,
)


class Command(BaseCommand):
    help = 'Добавляет зоны Standart/VIP, статусы, main_admin и club_admin'

    def handle(self, *args, **options):
        club, created = Club.objects.get_or_create(
            name='Главный клуб',
            defaults={
                'address': 'г. Москва, ул. Примерная, 1',
                'phone': '+7 (495) 000-00-00',
                'is_active': True,
            },
        )
        self.stdout.write(self.style.SUCCESS(
            f'Клуб: {club.name}' + (' (создан)' if created else '')
        ))

        for name, desc, price in [
            ('Standart', 'Стандартная зона', 150),
            ('VIP', 'VIP-зона с премиум-оборудованием', 300),
        ]:
            zone, created = ComputerZone.objects.get_or_create(
                club=club,
                name=name,
                defaults={'description': desc, 'hourly_price': price},
            )
            self.stdout.write(self.style.SUCCESS(
                f'Зона: {zone.name}' + (' (создана)' if created else '')
            ))

        for name, desc in [
            ('Активен', 'Компьютер свободен и готов к работе'),
            ('Не активен', 'Компьютер недоступен (обслуживание / выключен)'),
        ]:
            st, created = ComputerStatus.objects.get_or_create(
                name=name,
                defaults={'description': desc},
            )
            self.stdout.write(self.style.SUCCESS(
                f'Статус ПК: {st.name}' + (' (создан)' if created else '')
            ))

        for name, desc in [
            ('Активна', 'Сессия идёт'),
            ('Завершена', 'Сессия успешно завершена'),
            ('Отменена', 'Сессия отменена'),
            ('Забронирована', 'Сессия забронирована на будущее'),
        ]:
            st, created = SessionStatus.objects.get_or_create(
                name=name,
                defaults={'description': desc},
            )
            self.stdout.write(self.style.SUCCESS(
                f'Статус сессии: {st.name}' + (' (создан)' if created else '')
            ))

        # main_admin — club_id ОБЯЗАТЕЛЬНО NULL
        self._upsert_employee(
            login='admin',
            password='admin123',
            full_name='Администратор системы',
            phone='+7 (900) 000-00-01',
            role='main_admin',
            club=None,
        )

        # club_admin — club_id ОБЯЗАТЕЛЕН
        self._upsert_employee(
            login='manager',
            password='manager123',
            full_name='Менеджер смены',
            phone='+7 (900) 000-00-02',
            role='club_admin',
            club=club,
        )

        self.stdout.write(self.style.SUCCESS('\nГотово.'))
        self.stdout.write('  Admin (main_admin):   login=admin   / password=admin123')
        self.stdout.write('  Manager (club_admin): login=manager / password=manager123')

    def _upsert_employee(self, login, password, full_name, phone, role, club):
        try:
            emp = Employee.objects.get(login=login)
            emp.full_name = full_name
            emp.phone = phone
            emp.password_hash = make_password(password)
            emp.role = role
            emp.club = club
            emp.is_active = True
            emp.save()
            self.stdout.write(self.style.SUCCESS(f'{role}: {login} (обновлён)'))
        except Employee.DoesNotExist:
            try:
                emp = Employee(
                    login=login,
                    full_name=full_name,
                    phone=phone,
                    password_hash=make_password(password),
                    role=role,
                    club=club,
                    is_active=True,
                )
                emp.save()
                self.stdout.write(self.style.SUCCESS(f'{role}: {login} (создан)'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при создании {login}: {e}'))
                try:
                    with connection.cursor() as cur:
                        cur.execute("""
                            SELECT pg_get_constraintdef(oid)
                            FROM pg_constraint
                            WHERE conname = 'check_employee_club_role'
                        """)
                        row = cur.fetchone()
                        if row:
                            self.stdout.write(self.style.WARNING(f'Ограничение: {row[0]}'))
                except Exception:
                    pass
                raise
