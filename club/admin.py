from django.contrib import admin
from .models import (
    Tariff, Service, Computer, Client, Club,
    ComputerStatus, SessionStatus, ComputerZone, Employee, Session
)

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes', 'price', 'is_active')
    list_filter = ('is_active',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')

@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('computer_number', 'zone', 'status', 'is_active')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'bonus_points', 'is_blocked')

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'is_active')

admin.site.register(ComputerStatus)
admin.site.register(SessionStatus)
admin.site.register(ComputerZone)
admin.site.register(Employee)
admin.site.register(Session)
