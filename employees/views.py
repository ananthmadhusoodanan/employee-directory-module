from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Employee
from .forms import EmployeeForm


# Employee List
def employee_list(request):

    department = request.GET.get('department')

    employees = Employee.objects.all()

    if department:
        employees = employees.filter(
            Department__icontains=department
        )

    paginator = Paginator(employees, 5)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'employee_list.html',
        {
            'page_obj': page_obj
        }
    )


# Employee Detail
def employee_detail(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    return render(
        request,
        'employee_detail.html',
        {
            'employee': employee
        }
    )


# Add Employee
def add_employee(request):

    if request.method == "POST":

        form = EmployeeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Employee added successfully."
            )

            return redirect(
                'employee_list'
            )

    else:

        form = EmployeeForm()

    return render(
        request,
        'add_employee.html',
        {
            'form': form
        }
    )


# Edit Employee
def edit_employee(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    if request.method == "POST":

        form = EmployeeForm(
            request.POST,
            request.FILES,
            instance=employee
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Employee updated successfully."
            )

            return redirect(
                'employee_detail',
                pk=employee.pk
            )

    else:

        form = EmployeeForm(
            instance=employee
        )

    return render(
        request,
        'edit_employee.html',
        {
            'form': form,
            'employee': employee
        }
    )


# Delete Employee
def delete_employee(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    if request.method == "POST":

        employee.delete()

        messages.success(
            request,
            "Employee deleted successfully."
        )

        return redirect(
            'employee_list'
        )

    return render(
        request,
        'delete_employee.html',
        {
            'employee': employee
        }
    )

