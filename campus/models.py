from django.db import models

class Campus(models.Model):
    campus_name = models.CharField(max_length=100)
    campus_address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.campus_name

class Department(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='departments')
    dep_name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.dep_name}"