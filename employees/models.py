
from django.db import models


class Employee(models.Model):

    Employee_ID = models.AutoField(
        primary_key=True
    )

    Full_Name = models.CharField(
        max_length=100
    )

    Department = models.CharField(
        max_length=50
    )

    Email = models.EmailField(
        unique=True
    )

    Phone_Number = models.CharField(
        max_length=10
    )

    Designation = models.CharField(
        max_length=50
    )

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive")
    ]

    Status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Active"
    )

    Date_Joined = models.DateField()

    img = models.ImageField(
        upload_to='employees/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.Full_Name

