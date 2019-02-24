from django.db import models

class Office(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Unit(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Designation(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name        = models.CharField(max_length=100)
    birthdate   = models.DateField(null=True, blank=True)
    office      = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True)
    unit        = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    department  = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name