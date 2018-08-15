from django.contrib import admin
from .models import ReadNums, ReadDetail
# Register your models here.

@admin.register(ReadNums)
class ReadNumsAdmin(admin.ModelAdmin):
    list_display = ('read_nums', 'content_object', 'content_type',)

@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ('date', 'read_nums', 'content_object', 'content_type',)
