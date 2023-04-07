from django.shortcuts import render,redirect

from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from employee.models import *
from account.models import *
from django.db.models import ProtectedError
from datetime import date,datetime


# Create your views here.
def register_view(request, role):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = role

        if not username or not email or not password1 or not password2:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('register', role)

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('register', role)

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email id is already exist.')
            return redirect('register', role)

        if password1 == password2:

            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password2,
                role=role
            )



    return render(request, 'account/register.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')




def Dashboard(request):
    month = datetime.today().month
    if request.user.role == 3:
        fk_user       = CustomUser.objects.get(id=request.user.id)
        emp_obj       = Employee.objects.get(fk_user=fk_user)
        task_complete = Task.objects.filter(status='completed',fk_employee=emp_obj).count()
        task_pending  = Task.objects.filter(status='pending',fk_employee=emp_obj).count()
        total_task    = Task.objects.filter(created_at__month=month,fk_employee=emp_obj).count()
        task          = Task.objects.filter(fk_employee=emp_obj).order_by('-created_at')
        
    else:
        task          = Task.objects.filter(created_at__month=month,status='pending').order_by('-created_at')
        task_complete =  Task.objects.filter(status='completed').count()
        task_pending  =  Task.objects.filter(status='pending').count()
        total_task    =  Task.objects.filter(created_at__month=month).count()

    employee = Employee.objects.all().order_by('-created_at')
    employee_count = Employee.objects.all().count()
    context = {
        'employee_count': employee_count,
        'task_complete' : task_complete,
        'task_pending'  : task_pending,
        'total_task'    : total_task,
        'employee'      : employee,
        'tasks'         : task,

    }
    return render(request, 'account/dashboard.html',context)



def DepartmentList(request):
    dept = Department.objects.all().order_by('-created_at')
    context = {
        'department' : dept,
    }
    return render(request, 'account/departmentList.html',context)


def DepartmentAdd(request):

    if request.method == 'POST':
        deptName = request.POST.get('dept_name')
        Department.objects.create(
            DeptName=deptName,
        )

    return render(request, 'account/departmentAdd.html')


def DeptDelete(request,id):
    dept=Department.objects.get(id=id)
    dept.delete()

    return redirect('departmentList')



def base(request):
    user = CustomUser.objects.get(id=request.user.id)
    if user.role !=1 :

        profile = Employee.objects.get(fk_user=user)
    context={'profile': profile}
    
    
    return render(request, 'account/base.html',context)



def composeMessageView(request):
    employee = Employee.objects.all()
    fk_user = CustomUser.objects.get(id=request.user.id)
    # emp_obj = Employee.objects.get(fk_user=fk_user)
    if request.method == 'POST':
        to = request.POST.get('to')
        from_user = fk_user
        to_user = Employee.objects.get(id=to)
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Message.objects.create(
            message=message,
            subject=subject,
            fk_to=to_user,
            fk_from=fk_user

        )
        messages.success(request, 'message sent')

    context = {
        'employee': employee
    }
    return render(request, 'account/compose_mail.html', context)


def inboxMessageView(request):
    if request.user.role == 2 or request.user.role == 3:
        employee = Employee.objects.all()
        fk_user = CustomUser.objects.get(id=request.user.id)
        emp_obj = Employee.objects.get(fk_user=fk_user)
        msg = Message.objects.filter(fk_to=emp_obj)
    else :
        msg = Message.objects.all()
    context = {
        'messages': msg
    }
    return render(request, 'account/inbox.html', context)

def messageDeleteView(request,id):
    msg = Message.objects.get(id=id)
    msg.delete()
    return redirect('inbox')


def notification_add_view(request):
    if request.method == 'POST':
        title = request.POST.get('notification_title')
        news = request.POST.get('notification')
        if title :
            news_obj = Notification.objects.create(news_title=title,news_data=news)
            news_obj.save()
            messages.success(request, 'Notification Added.')

    today = date.today()
    year = datetime.today().year
    month = today.strftime("%m")
    news_obj = Notification.objects.filter(created_at__month=month,created_at__year=year)
    context ={
        
        'news_list' : news_obj
    }

    return render(request, 'account/notification_add.html',context=context)



#news delete view


def notification_delete_view(request,id):
    news = Notification.objects.get(id=id)

    try:
        news.delete()
        messages.success(request, 'Notification has been deleted.')
        return redirect('notification_add')
    except ProtectedError:
        messages.warning(
            request,
            "Notification has not been deleted.Reference exists.")
        return redirect('notification_add')