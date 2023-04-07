from django.shortcuts import render,redirect

from account.models import *
from django.contrib import messages
from .forms import *
from datetime import date,datetime
# Create your views here.


def addEmployeeView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')
        if not username or not email or not password1 or not password2:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('addEmployee')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('addEmployee')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email id is already exist.')
            return redirect('addEmployee')

        if password1 == password2:

            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password2,
                role=role
            )

        context ={
            'department':Department.objects.all()
        }
        dept = None  # assign a default value to dept
        emp_form_obj = EmployeeForm(request.POST, request.FILES)
        try:
            dept = Department.objects.get(id=request.POST.get('department'))
        except Department.DoesNotExist:  # use the full class name here
            messages.warning(request, "oops! You forget to select department")
            return redirect('addEmployee')

        if emp_form_obj.is_valid():
            emp_obj = emp_form_obj.save(commit=False)
            emp_obj.fk_department = dept
            emp_obj.fk_user = user
            emp_obj.save()

            Attendance.objects.create(
                fk_employee=emp_obj
            )

            messages.success(request, 'employee has been saved')
        else:
            messages.warning(request, emp_form_obj.errors)
        return redirect('addEmployee')
    context ={
        'department':Department.objects.all()
    }
    return render(request,'employee/add_Employee.html',context)



def ProfileView(request):
    user = CustomUser.objects.get(id=request.user.id)
    if user.role == 1:
        profile =user
    else :
        profile = Employee.objects.get(fk_user=user)
    if request.method == 'POST':
        current_password = request.POST.get('password')
        if current_password == user.password:

            password = request.POST.get('newpassword')
            confirm_password = request.POST.get('renewpassword')
            if password == confirm_password:
                user.set_password(password)
                user.save()

                messages.info(
                    request, 'Password has been updated, Please login to continue')
                return redirect('logout')

            else:
                messages.warning(request, 'Passwords are not matching')
                return redirect('profile', id=id)
        else:
            messages.warning(request, 'Current Passwords is not matching')
            return redirect('profile', id=id)

    context = {
        'profile' : profile,
    }
    return render(request, 'employee/profile.html',context)




def employeeListView(request):
    emp = Employee.objects.all().order_by('-created_at')
    context = {
        'employee' : emp,
    }
    return render(request, 'employee/employee_List.html',context)



def employeeDeleteView(request,id):
    emp = Employee.objects.get(id=id)
    emp.delete()

    return redirect('employeeList')



def employeeEditView(request,id):
    employee = Employee.objects.get(id=id)
    user = CustomUser.objects.get(id=employee.fk_user.id)
    if request.method == 'POST':
        emp_form_obj = EmployeeForm(request.POST, request.FILES,instance=employee)
        try:
            dept = Department.objects.get(id=request.POST.get('department'))
        except :
            messages.warning(request, "oops! You forget to select department")
            return redirect('employeeEdit',id=id)
        if emp_form_obj.is_valid():
            emp_obj = emp_form_obj.save(commit=False)
            emp_obj.fk_department = dept
            emp_obj.fk_user = user
            emp_obj.save()
            messages.success(request, 'employee has been saved')
            return redirect('employeeList')
        else:
            messages.warning(request, emp_form_obj.errors)
        return redirect('employeeEdit',id=id)
    context = {
        'department': Department.objects.all(),
        'employee':employee
    }
    return render(request, 'employee/edit_Employee.html', context)


def addTaskView(request):

    if request.method == 'POST':
        task = request.POST.get('task')
        last_date = request.POST.get('last_date')
        emp_id = request.POST.get('empId')
        task_pdf = request.FILES['myfile']
        print(emp_id)
        emp_obj = Employee.objects.get(id=emp_id)
        Task.objects.create(
            task=task,
            last_date=last_date,
            fk_employee=emp_obj,
            task_pdf=task_pdf
        )
        messages.success(request, 'task added')
        return redirect('employeeList')
    return render(request, 'task_List.html')

def TaskListView(request):
    if request.user.role == 3:
        fk_user = CustomUser.objects.get(id=request.user.id)
        emp_obj = Employee.objects.get(fk_user=fk_user)
        task = Task.objects.filter( fk_employee=emp_obj)
    else :
        task = Task.objects.all().order_by('-created_at')
    context = {
        'tasks' : task,
    }
    return render(request, 'employee/task_List.html',context)





def taskDeleteView(request,id):
    task = Task.objects.get(id=id)
    task.delete()

    return redirect('taskList')

def changeTaskStatusView(request):

    if request.method == 'POST':
        status = request.POST.get('status')
        id = request.POST.get('taskId')
        task = Task.objects.get(id=id)
        task.status = status
        task.save()

    return redirect('taskList')


def addAttendanceView(request):

    departments = Department.objects.all()
    employee_list = Attendance.objects.all().order_by('-created_at')
    search_date = datetime.now().date()
    if request.method == 'POST':
        search_dept = request.POST.get('search_dept')
        search_emp = request.POST.get('search_emp')
        search_date = request.POST.get('fdate')
        search_tdate = request.POST.get('tdate')
        if search_dept :
            search_date = datetime.now().date()
            employee_list = Attendance.objects.filter(fk_employee__fk_department__DeptName=search_dept).order_by('-created_at')
        elif search_emp:
            search_date = datetime.now().date()
            employee_list = Attendance.objects.filter(fk_employee__e_name=search_emp).order_by('-created_at')
        elif search_date:
            employee_list = Attendance.objects.filter(Date=search_date).order_by('-created_at')

        elif search_dept and search_emp :
            search_date = datetime.now().date()
            employee_list = Attendance.objects.filter(fk_employee__e_name=search_emp,fk_employee__fk_department__DeptName=search_dept).order_by('-created_at')
        elif search_dept and search_emp and search_date :
            employee_list = Attendance.objects.filter(fk_employee__fk_department__DeptName=search_dept,Date=search_date).order_by('-created_at')

    context ={
        'attendance' :employee_list,
        'departments' : departments,
        'date' : search_date
    }
    return render(request,'employee/attendanceAdd.html',context)



def ChangeAttendanceView(request, id):
    attnd = Attendance.objects.get(id=id)
    attnd.Presence = not attnd.Presence
    attnd.save()
    return redirect('addAttendance')


def addSalaryView(request):

    if request.method == 'POST':
        salary = request.POST.get('salary')
        emp_id = request.POST.get('empId')
        emp_obj = Employee.objects.get(id=emp_id)
        Salary.objects.create(
            salary=salary,
            fk_employee=emp_obj
        )
        messages.success(request, 'salary added')
    return redirect('employeeList')

def SalaryListView(request):
    salary = Salary.objects.all().order_by('-created_at')
    context = {
        'salary' : salary,
    }
    return render(request, 'employee/salary_List.html',context)

def SalaryDeleteView(request,id):
    salary = Task.objects.get(id=id)
    salary.delete()

    return redirect('salaryList')


def changeSalaryStatusView(request):

    if request.method == 'POST':
        status = request.POST.get('status')
        id = request.POST.get('salaryId')
        salary = Salary.objects.get(id=id)
        salary.status = status
        salary.save()

    return redirect('salaryList')