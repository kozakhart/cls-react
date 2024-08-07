# Generated by Django 4.0.6 on 2022-08-25 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OPIForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agree', models.BooleanField()),
                ('entry_date', models.DateField(auto_now_add=True)),
                ('entry_time', models.TimeField(auto_now_add=True)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('byuid', models.CharField(max_length=9)),
                ('netid', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('reason', models.CharField(choices=[('', ''), ('CHIN 495', 'CHIN 495'), ('FLAS Pre-test', 'FLAS Pre-test'), ('FLAS Post-test', 'FLAS Post-test'), ('FLANG 300 (Dual Language Immersion)', 'FLANG 300 (Dual Language Immersion)'), ('FREN 495', 'FREN 495'), ('GERM 400', 'GERM 400'), ('Individual Request', 'Individual Request'), ('ITAL 491', 'ITAL 491'), ('JAPAN 495', 'JAPAN 495'), ('KOREA 491', 'KOREA 491'), ('Lanuage Certificate', 'Lanuage Certificate'), ('Language Teaching Major/Minor', 'Language Teaching Major/Minor'), ('PORT 491', 'PORT 491'), ('RUSS 492', 'RUSS 492'), ('SLaT Applicant or Program Requirement', 'SLaT Applicant or Program Requirement'), ('SPAN 491', 'SPAN 491'), ('Study Abroad Pre-test', 'Study Abroad Pre-test'), ('Study Abroad Post-test', 'Study Abroad Post-test'), ('Other', 'Other')], default='', max_length=100)),
                ('reason_other', models.CharField(max_length=100)),
                ('language', models.CharField(choices=[('', ''), ('Arabic', 'Arabic'), ('Dutch', 'Dutch'), ('English', 'English'), ('Finnish', 'Finnish'), ('French', 'French'), ('Mandarin', 'Mandarin'), ('German', 'German'), ('Indonesian', 'Indonesian'), ('Italian', 'Italian'), ('Japanese', 'Japanese'), ('Korean', 'Korean'), ('Norwegian', 'Norwegian'), ('Portuguesse', 'Portuguese'), ('Russian', 'Russian'), ('Spanish', 'Spanish'), ('Tagalog', 'Tagalog'), ('Thai', 'Thai'), ('Vietnamese', 'Vietnamese'), ('Haitian Creole', 'Haitian Creole'), ('Other', 'Other')], default='', max_length=100)),
                ('language_other', models.CharField(max_length=100)),
                ('experience', models.CharField(choices=[('', ''), ('Mission', 'Mission'), ('Native speaker', 'Native speaker'), ('Heritage speaker (you learned it at home, through family members', 'Heritage speaker (you learned it at home, through family members'), ('Beginner', 'Beginner'), ('Professional', 'Professional'), ('Learned through University/High School Courses', 'Learned through University/High School Courses')], default='', max_length=100)),
                ('major', models.CharField(max_length=100)),
                ('second_major', models.CharField(max_length=100)),
                ('minor', models.CharField(max_length=100)),
                ('graduate', models.DateField(max_length=100)),
                ('scores', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('come_to_campus', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('cannot_come', models.CharField(choices=[('NA', 'NA'), ('Quarantine/Medical Reason', 'Quarantine/Medical Reason'), ('Located outside of Utah County', 'Located outside of Utah County')], max_length=100)),
                ('testdate1', models.DateField(max_length=100)),
                ('time1', models.TimeField()),
                ('time2', models.TimeField()),
                ('testdate2', models.DateField(max_length=100)),
                ('time3', models.TimeField()),
                ('time4', models.TimeField()),
                ('confirm_email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
            ],
        ),
    ]
