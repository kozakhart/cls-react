from django.db import models
import myapp.model_choices as mc
from django import forms
from django.contrib.auth.models import User
import subprocess


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

class SLATForm(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    byuid = models.CharField(max_length=9)
    language = models.CharField(max_length=100, choices= mc.slat.languages, default='')
    thesis = models.DateField()
    transcript = models.FileField()
    opi = models.FileField()

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

# class OPI_Signin(models.Model):
#     password = models.CharField(max_length=6)

class HeardAbout(models.Model):
    heard_about = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Heard About"
    def __str__(self):
        return self.heard_about

class Degrees(models.Model):
    degree = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Degrees"
    def __str__(self):
        return self.degree
    
class SemesterOfEntry(models.Model):
    semester = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Semester of Entry"
    def __str__(self):
        return self.semester
    
class Scores(models.Model):
    score = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Scores"
    def __str__(self):
        return self.score
    
class AcademicStatus(models.Model):
    status = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Academic Status"
    def __str__(self):
        return self.status

class MAPLForm(models.Model):
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    byuid = models.CharField(max_length=9)
    phone = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    heard_about = models.ForeignKey('HeardAbout', on_delete=models.CASCADE)
    semester_of_entry = models.ForeignKey('SemesterOfEntry', on_delete=models.CASCADE)
    gpa = models.CharField(max_length=100)
    location_of_experience = models.TextField()
    location_from_date = models.DateField()
    location_to_date = models.DateField()
    opi_score = models.ForeignKey('Scores', related_name='mapl_opi_scores', on_delete=models.CASCADE)
    opi_date = models.DateField()
    wpt_score = models.ForeignKey('Scores', related_name='mapl_wpt_scores', on_delete=models.CASCADE)
    wpt_date = models.DateField()
    alt_score = models.ForeignKey('Scores', related_name='mapl_alt_scores', on_delete=models.CASCADE)
    alt_date = models.DateField()
    art_score = models.ForeignKey('Scores', related_name='mapl_art_scores', on_delete=models.CASCADE)
    art_date = models.DateField()
    other_test_name = models.CharField(max_length=100)
    other_test_score = models.CharField(max_length=100)
    other_test_date = models.DateField()
    institution_name = models.CharField(max_length=100)
    institution_location = models.CharField(max_length=100)
    institution_from_date = models.DateField()
    institution_to_date = models.DateField()
    degree = models.ForeignKey('Degrees', on_delete=models.CASCADE)
    graduation_date = models.DateField()
    recommender_name_1 = models.CharField(max_length=100)
    recommender_title_1 = models.CharField(max_length=100)
    recommender_institution_1 = models.CharField(max_length=100)
    recommender_email_1 = models.EmailField(max_length=100)
    recommender_phone_1 = models.CharField(max_length=100)
    recommender_name_2 = models.CharField(max_length=100)
    recommender_title_2 = models.CharField(max_length=100)
    recommender_institution_2 = models.CharField(max_length=100)
    recommender_email_2 = models.EmailField(max_length=100)
    recommender_phone_2 = models.CharField(max_length=100)
    statement_of_purpose = models.FileField()
    student_signature = models.CharField(max_length=100)
    student_date = models.DateField()
    academic_status = models.ForeignKey('AcademicStatus', on_delete=models.CASCADE)