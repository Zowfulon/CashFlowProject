from django.contrib import admin
from nested_admin import nested

from money_addition_notes.models import MoneyAdditionNote, MoneyAdditionStatus, \
    MoneyAdditionType, MoneyAdditionCategory, MoneyAdditionSubCategory


# Register your models here.

# @admin.register(MoneyAdditionNote)
# class MoneyAdditionNoteAdmin(nested.NestedModelAdmin):
#     fields = (
#         'date_created', ('status', 'money_type', 'category', 'subcategory'),
#         'money_value', 'comment')


@admin.register(MoneyAdditionStatus)
class MoneyAdditionStatusAdmin(nested.NestedModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class MoneyAdditionSubCategoryInline(nested.NestedTabularInline):
    model = MoneyAdditionSubCategory
    extra = 0
    prepopulated_fields = {'slug': ('name',)}


class MoneyAdditionCategoryInline(nested.NestedTabularInline):
    model = MoneyAdditionCategory
    inlines = [MoneyAdditionSubCategoryInline]
    extra = 0
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MoneyAdditionType)
class MoneyAdditionTypeAdmin(nested.NestedModelAdmin):
    """Таблица управления справочниками реализована в административной
    панели с помощью модуля django-nested-admin для допуска использования
    свыше одного уровня"""
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MoneyAdditionCategoryInline]
