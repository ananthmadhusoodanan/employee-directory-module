from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Employee
from .forms import EmployeeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import csv
import io
from datetime import datetime

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Employee

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Employee

# Employee List

@login_required
def employee_list(request):

    department = request.GET.get('department')

    employees = Employee.objects.filter(
        user=request.user
    )

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
        {'page_obj': page_obj}
    )

# Employee Detail
@login_required
def employee_detail(request, pk):

    employee = get_object_or_404(
    Employee,
    pk=pk,
    user=request.user
)

    return render(
        request,
        'employee_detail.html',
        {
            'employee': employee
        }
    )


# Add Employee
@login_required
def add_employee(request):

    if request.method == "POST":

        form = EmployeeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            employee = form.save(commit=False)

            employee.user = request.user

            employee.save()

            messages.success(
                request,
                "Employee added successfully."
            )

            return redirect('employee_list')

    else:

        form = EmployeeForm()

    return render(
        request,
        'add_employee.html',
        {'form': form}
    )


# Edit Employee
@login_required
def edit_employee(request, pk):

    employee = get_object_or_404(
    Employee,
    pk=pk,
    user=request.user
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
@login_required
def delete_employee(request, pk):

    employee = get_object_or_404(
    Employee,
    pk=pk,
    user=request.user
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

def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():

            return render(
                request,
                "register.html",
                {
                    "error": "Username already exists"
                }
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(
        request,
        "register.html"
    )
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('employee_list')

        return render(
            request,
            'login.html',
            {'error': 'Invalid username or password'}
        )

    return render(request, 'login.html')
def logout_view(request):

    logout(request)

    return redirect("login")

from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):

    logout(request)

    return redirect('login')

@login_required
def download_csv(request):

    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = (
        'attachment; filename="employees.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Employee ID',
        'Full Name',
        'Department',
        'Email',
        'Phone Number',
        'Designation',
        'Status',
        'Date Joined'
    ])

    employees = Employee.objects.filter(user=request.user)

    for employee in employees:

        writer.writerow([
            employee.Employee_ID,
            employee.Full_Name,
            employee.Department,
            employee.Email,
            employee.Phone_Number,
            employee.Designation,
            employee.Status,
            employee.Date_Joined,
        ])

    return response

@login_required
def import_csv(request):

    if request.method != "POST":
        return redirect("employee_list")

    csv_file = request.FILES.get("csv_file")

    if not csv_file:

        messages.error(
            request,
            "Please select a CSV file."
        )

        return redirect("employee_list")

    if not csv_file.name.endswith(".csv"):

        messages.error(
            request,
            "Only CSV files are allowed."
        )

        return redirect("employee_list")

    try:

        file_data = csv_file.read().decode("utf-8")

        csv_reader = csv.DictReader(
            io.StringIO(file_data)
        )

        required_columns = [
            "Full_Name",
            "Department",
            "Email",
            "Phone_Number",
            "Designation",
            "Status",
            "Date_Joined",
        ]

        if not all(
            column in csv_reader.fieldnames
            for column in required_columns
        ):

            messages.error(
                request,
                "Invalid CSV format. Please check the column names."
            )

            return redirect("employee_list")

        imported_count = 0
        skipped_count = 0

        for row in csv_reader:

            if Employee.objects.filter(
                user=request.user,
                Email=row["Email"]
            ).exists():

                skipped_count += 1
                continue

            date_value = row["Date_Joined"].strip()

            date_joined = None

            for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y"):

                try:

                    date_joined = datetime.strptime(
                        date_value,
                        fmt
                    ).date()

                    break

                except ValueError:
                    continue

            if date_joined is None:

                messages.error(
                    request,
                    f"Invalid date format: {date_value}"
                )

                continue

            Employee.objects.create(
                user=request.user,
                Full_Name=row["Full_Name"].strip(),
                Department=row["Department"].strip(),
                Email=row["Email"].strip(),
                Phone_Number=row["Phone_Number"].strip(),
                Designation=row["Designation"].strip(),
                Status=row["Status"].strip(),
                Date_Joined=date_joined
            )

            imported_count += 1

        messages.success(
            request,
            f"{imported_count} employees imported successfully."
        )

        if skipped_count:

            messages.warning(
                request,
                f"{skipped_count} employees were skipped because they already exist."
            )

    except Exception as e:

        messages.error(
            request,
            f"Error importing file: {str(e)}"
        )

    return redirect("employee_list")
