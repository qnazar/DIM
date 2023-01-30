from django.contrib import admin
from django.utils.html import format_html
from .models import Style, Category, Teacher, Group


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'salary')
    search_fields = ('name', )
    list_editable = ('salary', )


class StyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name', )
    search_fields = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'category', 'get_styles', 'photo', 'slug', 'show_link')
    list_filter = ('category', 'styles')
    search_fields = ('nickname', 'first_name', 'last_name', ',middle_name')
    prepopulated_fields = {
        'nickname': ('first_name', 'last_name'),
        'slug': ('nickname', )
    }
    filter_horizontal = ('styles', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('styles')

    def get_styles(self, teacher):
        return ', '.join([s.name for s in teacher.styles.all()])
    get_styles.short_description = 'Стилі'

    def show_link(self, teacher):
        return format_html(f'<a href="{teacher.get_absolute_url()}">На сторінку</a>')
    show_link.short_description = 'Сторінка'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'style', 'level', 'scheduled_time', 'get_days', 'duration', 'is_active')
    list_filter = ('teacher', 'style', 'level')
    list_editable = ('is_active', )
    search_fields = ('teacher', 'style')

    def get_days(self, group):
        return group.get_days
    get_days.short_description = 'Дні'


admin.site.register(Style, StyleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Group, GroupAdmin)
