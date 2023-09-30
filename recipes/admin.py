from django.contrib import admin

from .models import Recipe, Step

admin.site.register(Recipe)
admin.site.register(Step)
