from django.contrib import admin
from .models import Employee,Department,Designation,Unit,Office
# Register your models here.
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Unit)
admin.site.register(Office)
