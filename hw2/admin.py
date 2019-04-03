from django.contrib import admin

from .models import Book

from import_export.admin import ImportExportModelAdmin

@admin.register(Book)
class ViewAdmin(ImportExportModelAdmin):
    pass