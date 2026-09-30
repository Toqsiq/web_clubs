from django.db import models


class ComputerStatus(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField()

    class Meta:
        db_table = 'computer_statuses'
        managed = False

    def __str__(self):
        return self.name


class SessionStatus(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField()

    class Meta:
        db_table = 'session_statuses'
        managed = False

    def __str__(self):
        return self.name


class Club(models.Model):
    name = models.TextField()
    address = models.TextField()
    phone = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'clubs'
        managed = False

    def __str__(self):
        return self.name


class Tariff(models.Model):
    name = models.TextField()
    duration_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tariffs'
        managed = False

    def __str__(self):
        return f"{self.name} — {self.price} ₽"


class Service(models.Model):
    name = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'services'
        managed = False

    def __str__(self):
        return f"{self.name} — {self.price} ₽"


class ComputerZone(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, db_column='club_id')
    name = models.TextField()
    description = models.TextField()
    hourly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'computer_zones'
        managed = False

    def __str__(self):
        return self.name


class Computer(models.Model):
    computer_number = models.IntegerField()
    zone = models.ForeignKey(ComputerZone, on_delete=models.CASCADE, db_column='zone_id')
    status = models.ForeignKey(ComputerStatus, on_delete=models.CASCADE, db_column='status_id')
    cpu = models.TextField()
    gpu = models.TextField()
    ram_gb = models.IntegerField()
    storage_gb = models.IntegerField()
    monitor = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'computers'
        managed = False

    def __str__(self):
        return f"ПК №{self.computer_number}"


class Client(models.Model):
    full_name = models.TextField()
    phone = models.TextField(unique=True)
    email = models.TextField(unique=True)
    registration_date = models.DateTimeField()
    bonus_points = models.IntegerField(default=0)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        db_table = 'clients'
        managed = False

    def __str__(self):
        return self.full_name


class Employee(models.Model):
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, db_column='club_id')
    full_name = models.TextField()
    phone = models.TextField()
    login = models.TextField(unique=True)
    password_hash = models.TextField()
    role = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'employees'
        managed = False

    def __str__(self):
        return self.full_name


class Session(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='client_id')
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE, db_column='computer_id')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, db_column='tariff_id')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_id')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.ForeignKey(SessionStatus, on_delete=models.CASCADE, db_column='status_id')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.TextField()
    payment_status = models.TextField()
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'sessions'
        managed = False

    def __str__(self):
        return f"Сессия #{self.id}"
