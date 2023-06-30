from django.contrib import admin
from . models import *

from django.contrib.admin import  ModelAdmin
# Register your models here.
class CategoryAdmin(ModelAdmin):
    prepopulated_fields = {'slug':("category_name",)}
    list_display = ('category_name','slug')
admin.site.register(category,CategoryAdmin)
