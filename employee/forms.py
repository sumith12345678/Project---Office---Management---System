from django.forms import ModelForm
from  account . models import *

from . models import *


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        exclude = ('fk_user','fk_department')