from django.db import models
import myapp.model_choices as mc

class Languages(models.Model):
    full_language = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Languages"
    def __str__(self):
        return self.full_language

class LanguageExperience(models.Model):
    experience = models.CharField(max_length=100)

    def __str__(self):
        return self.experience

class ComeToCampusReason(models.Model):
    campusreason = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Campus Reasons"
    def __str__(self):
        return self.campusreason

class Reasons(models.Model):
    reason = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Reasons"
    def __str__(self):
        return self.reason

class OPIForm(models.Model):
    
    agree = models.BooleanField()
    entry_date = models.DateField(auto_now_add=True)
    entry_time = models.TimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    byuid = models.CharField(max_length=9)
    netid = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    reason = models.ForeignKey('Reasons', on_delete=models.CASCADE)
    reason_other = models.CharField(max_length=100)
    language = models.ForeignKey('Languages', on_delete=models.CASCADE)
    language_other = models.CharField(max_length=100)
    experience = models.ForeignKey('LanguageExperience', on_delete=models.CASCADE)
    major = models.CharField(max_length=100)
    second_major = models.CharField(max_length=100)
    minor = models.CharField(max_length=100)
    scores = models.CharField(choices= mc.choices.yes_no, max_length=10)
    come_to_campus = models.CharField(choices= mc.choices.yes_no, max_length=10)
    cannot_come = models.ForeignKey('ComeToCampusReason', on_delete=models.CASCADE)
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