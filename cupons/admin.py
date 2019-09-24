from django.contrib import admin
from .models import Cupon


class CuponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter  = ['valid_from', 'valid_to', 'active']
    search_field = ['code']


admin.site.register(Cupon, CuponAdmin)
