from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "client", "Client"
        SUPPLIER = "supplier", "Supplier"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT
    )

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.city}, {self.street}, {self.house}"