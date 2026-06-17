from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='employees'
    )

    Employee_ID = models.AutoField(primary_key=True)

    Full_Name = models.CharField(max_length=100)

    Department = models.CharField(max_length=50)

    Email = models.EmailField(unique=True)

    Phone_Number = models.CharField(max_length=10)

    Designation = models.CharField(max_length=50)

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
    
from datetime import timedelta


class Leave(models.Model):

    LEAVE_TYPES = [
        ("Casual", "Casual"),
        ("Sick", "Sick"),
        ("Annual", "Annual"),
        ("Work From Home", "Work From Home"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="leaves"
    )

    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPES
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    applied_on = models.DateTimeField(auto_now_add=True)

    @property
    def total_days(self):

        return (
            self.end_date - self.start_date
        ).days + 1