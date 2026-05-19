import hashlib

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=120)
    hashed_password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, default="user")

    def set_password(self, password):
        self.hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

    def check_password(self, password):
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return self.hashed_password == password_hash

    def __str__(self):
        return f"{self.full_name}: {self.role}"


class FuelType(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class FuelItem(models.Model):
    name = models.CharField(max_length=120)
    supplier = models.CharField(max_length=120)
    quantity_liters = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    fuel_type = models.ForeignKey(FuelType, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class IssueRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    fuel_item = models.ForeignKey(FuelItem, on_delete=models.PROTECT)
    amount_liters = models.PositiveIntegerField()
    destination = models.CharField(max_length=150)
    issued_at = models.DateTimeField()

    def __str__(self):
        return f"{self.fuel_item.name}: {self.amount_liters} л"
