from django.db import models

# Create your models here.
class Language(models.Model):
    language = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Languages"
    def __str__(self):
        return self.language
    
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
    
class BachelorsCompletion(models.Model):
    degree_completion = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Will Bachelor's Be Completed?"

    def __str__(self):
        return self.degree_completion
    
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
    language = models.ForeignKey('Language', on_delete=models.CASCADE, null=True)
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
    bachelors_completion = models.ForeignKey('BachelorsCompletion', on_delete=models.CASCADE, null=True)
    graduation_date = models.DateField()
    coursework_explanation = models.CharField(max_length=100, default='')
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