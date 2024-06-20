from django.contrib import admin

# Register your models here.

from .models import LASER_Queries

models = [LASER_Queries]
for model in models:
    admin.site.register(model)
