from django.db import models
from django.contrib.auth.models import User

class Students(models.Model):
    class Meta:
        verbose_name_plural = "Students"
    agree = models.BooleanField()
    entry_date = models.DateField(auto_now_add=True)
    entry_time = models.TimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    byuid = models.CharField(max_length=9)
    netid = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    reason = models.CharField(max_length=100)
    reason_other = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    language_other = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    second_major = models.CharField(max_length=100)
    minor = models.CharField(max_length=100)
    scores = models.CharField(max_length=100)
    come_to_campus = models.CharField(max_length=100)
    cannot_come = models.CharField(max_length=100)
    testdate1 = models.DateField(max_length=100)
    time1 = models.TimeField()
    time2 = models.TimeField()
    testdate2 = models.DateField(max_length=100)
    time3 = models.TimeField()
    time4 = models.TimeField()
    CertificateStatus = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)

    #This is how the objects display on the admin frontend
    def __str__(self):
        return '{} {} {} {}'.format(self.firstname, self.lastname, self.entry_date, self.entry_time)
    

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

class LASER_Queries(models.Model):
    query_label = models.CharField(max_length=100, default="", blank=True, null=True)
    query = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Laser Queries"
        verbose_name_plural = "Laser Queries"
    def __str__(self):
        return '{}'.format(self.query_label)
    
class OPIc_Diagnostic_Grid_Languages(models.Model):
    language = models.CharField(max_length=100)
    class Meta:
        verbose_name = "OPIc Diagnostic Grid Languages"
        verbose_name_plural = "OPIc Diagnostic Grid Languages"
    def __str__(self):
        return '{}'.format(self.language)