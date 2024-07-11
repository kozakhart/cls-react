from django.contrib import admin

# Register your models here.

from .models import LASER_Queries, OPIc_Diagnostic_Grid_Languages

models = [LASER_Queries]
for model in models:
    admin.site.register(model)
