from django.contrib import admin

from .models import (
    Genre,
    Category,
    Title,
)

EMPTY_VALUE_DISPLAY = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_editable = ('name', 'slug',)
    search_fields = ('name', 'slug')
    empty_value_display = EMPTY_VALUE_DISPLAY


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_editable = ('name', 'slug',)
    search_fields = ('name', 'slug')
    empty_value_display = EMPTY_VALUE_DISPLAY


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
    )
    list_editable = ('name', 'year', 'category')
    search_fields = ('name', 'year', 'category')
    list_filter = ('year',)
    empty_value_display = EMPTY_VALUE_DISPLAY


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
