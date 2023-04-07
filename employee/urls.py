from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('addEmployee', addEmployeeView, name='addEmployee'),
    path('profile',ProfileView,name='profile'),
    path('employeeList', employeeListView, name='employeeList'),
    path('employeeDelete/<int:id>',employeeDeleteView,name='employeeDelete'),
    path('employeeEdit/<int:id>',employeeEditView,name='employeeEdit'),
    
    
    path('addTask', addTaskView, name='addTask'),
    path('taskList', TaskListView, name='taskList'),
    path('taskDelete/<int:id>',taskDeleteView,name='taskDelete'),
    path('changeTaskStatus', changeTaskStatusView, name='changeTaskStatus'),
    
    path('addAttendance',addAttendanceView,name='addAttendance'),
    path('changeAttendanceStatus/<int:id>',ChangeAttendanceView,name='ChangeAttendance'),
    
    path('addSalary', addSalaryView, name='addSalary'),
    path('salaryList', SalaryListView, name='salaryList'),
    path('changeSalaryStatus', changeSalaryStatusView, name='changeSalaryStatus'),
    path('salaryDelete/<int:id>',SalaryDeleteView,name='salaryDelete'),
    
    
    
   
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)