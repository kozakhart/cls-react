from django.contrib import admin
from .models import *

# Register your models here.
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

class DegreesAdmin(admin.ModelAdmin):
    model = Degrees
    def save_model(self, request, obj, form, change):        
        super().save_model(request, obj, form, change)

        return obj.degree
    def delete_model(self, request, obj):

        obj.delete()
admin.site.register(Degrees, DegreesAdmin)

class LanguageAdmin(admin.ModelAdmin):
    model = Language
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        return obj.language
    def delete_model(self, request, obj):

        obj.delete()
admin.site.register(Language, LanguageAdmin)

class BachelorsCompletionAdmin(admin.ModelAdmin):
    model = BachelorsCompletion
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        return obj.degree_completion
    def delete_model(self, request, obj):

        obj.delete()
admin.site.register(BachelorsCompletion, BachelorsCompletionAdmin)
