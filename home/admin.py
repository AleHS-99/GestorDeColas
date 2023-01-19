from django.contrib import admin
from.models import *
# Register your models here.

class ColaAdmin(admin.ModelAdmin):
    readonly_fields =('creada_por','codigo',)

class itemAdmin(admin.ModelAdmin):
    readonly_fields = ('codigo','cola',)

admin.site.register(ColaModel,ColaAdmin)
admin.site.register(ColaItem,itemAdmin)
