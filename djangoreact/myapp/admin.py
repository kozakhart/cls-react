from django.contrib import admin
from django.shortcuts import render
from .models import OPIForm, Languages, Reasons, Degrees, LanguageExperience, ComeToCampusReason, HeardAbout, SemesterOfEntry, Scores, AcademicStatus
from .forms import OPIForm_Forms
import myapp.filemaker_api.filemaker_api as filemaker
import myapp.box_api.box_api as box
import pandas as pd


class LanguagesAdmin(admin.ModelAdmin):
    model = Languages
    def save_model(self, request, obj, form, change):        
        super().save_model(request, obj, form, change)

        return obj.full_language
    def delete_model(self, request, obj):

        obj.delete()

    
admin.site.register(Languages, LanguagesAdmin)

class DegreesAdmin(admin.ModelAdmin):
    model = Degrees
    def save_model(self, request, obj, form, change):        
        super().save_model(request, obj, form, change)

        return obj.degree
    def delete_model(self, request, obj):

        obj.delete()
admin.site.register(Degrees, DegreesAdmin)

class ReasonsAdmin(admin.ModelAdmin):
    model = Reasons
    def save_model(self, request, obj, form, change):        
        super().save_model(request, obj, form, change)

        return obj.reason
    def delete_model(self, request, obj):

        obj.delete()


admin.site.register(Reasons, ReasonsAdmin)

class LanguageExperienceAdmin(admin.ModelAdmin):
    model = LanguageExperience
    def save_model(self, request, obj, form, change):        
        super().save_model(request, obj, form, change)

        return obj.experience
    def delete_model(self, request, obj):

        obj.delete()

admin.site.register(LanguageExperience, LanguageExperienceAdmin)

class ComeToCampusReasonAdmin(admin.ModelAdmin):
    model = ComeToCampusReason
    def save_model(self, request, obj, form, change):        
        super().save_model(request, obj, form, change)

        return obj.campusreason
    def delete_model(self, request, obj):

        obj.delete()

admin.site.register(ComeToCampusReason, ComeToCampusReasonAdmin)

class HeardAboutAdmin(admin.ModelAdmin):
    model = HeardAbout
    def save_model(self, request, obj, form, change):        
        super().save_model(request, obj, form, change)

        return obj.heard_about
    def delete_model(self, request, obj):

        obj.delete()

admin.site.register(HeardAbout, HeardAboutAdmin)

class SemesterOfEntryAdmin(admin.ModelAdmin):
    model = SemesterOfEntry
    def save_model(self, request, obj, form, change):        
        super().save_model(request, obj, form, change)

        return obj.semester
    def delete_model(self, request, obj):

        obj.delete()
admin.site.register(SemesterOfEntry, SemesterOfEntryAdmin)

class ScoresAdmin(admin.ModelAdmin):
    model = Scores
    def save_model(self, request, obj, form, change):        
        super().save_model(request, obj, form, change)

        return obj.score
    def delete_model(self, request, obj):

        obj.delete()
admin.site.register(Scores, ScoresAdmin)

class AcademicStatusAdmin(admin.ModelAdmin):
    model = AcademicStatus
    def save_model(self, request, obj, form, change):        
        super().save_model(request, obj, form, change)

        return obj.status
    def delete_model(self, request, obj):

        obj.delete()
admin.site.register(AcademicStatus, AcademicStatusAdmin)



