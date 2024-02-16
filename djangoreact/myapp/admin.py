from django.contrib import admin
from django.shortcuts import render
from .models import OPIForm, Languages, Reasons, LanguageExperience, ComeToCampusReason, Courses
from .forms import OPIForm_Forms
import myapp.filemaker_api.filemaker_api as filemaker
import myapp.box_api.box_api as box
import pandas as pd


class CoursesAdmin(admin.ModelAdmin):
    search_fields = ['byu_course_key', 'language', 'language_abbreviation']
    list_filter = ['type_language', 'type_civilization_culture', 'type_literature']
    model = Courses

    def save_model(self, request, obj, form, change):        
        super().save_model(request, obj, form, change)

        return obj.byu_course_key
    def delete_model(self, request, obj):
        obj.delete()

admin.site.register(Courses, CoursesAdmin)

class LanguagesAdmin(admin.ModelAdmin):
    model = Languages
    def save_model(self, request, obj, form, change):        
        super().save_model(request, obj, form, change)

        return obj.full_language
    def delete_model(self, request, obj):

        obj.delete()

    
admin.site.register(Languages, LanguagesAdmin)

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




