from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import  *
# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','created_date','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}

class variationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value','is_active')

admin.site.register(product,productAdmin)
admin.site.register(variation,variationAdmin)