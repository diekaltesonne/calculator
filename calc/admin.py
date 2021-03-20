from django.contrib import admin
from .models import Truck, Storage

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ['name','model','carrying_capacity','max_carrying_capacity','percentage_SiO2', 'percentage_Fe']
    list_filter = ['carrying_capacity', 'percentage_SiO2', 'percentage_Fe']
    list_editable = ['carrying_capacity', 'percentage_SiO2', 'percentage_Fe']
@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'percentage_SiO2', 'percentage_Fe']
    list_filter = ['capacity', 'percentage_SiO2', 'percentage_Fe']
    list_editable = ['capacity', 'percentage_SiO2', 'percentage_Fe']
    
    
# Register your models here.
