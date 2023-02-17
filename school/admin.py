from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from .models import Style, Category, Teacher, Group, Abonement, Hall, AbonementItem, Lesson


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
    search_fields = ('nickname', )
    prepopulated_fields = {
        'slug': ('nickname', )
    }
    filter_horizontal = ('styles', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('styles').select_related('category')

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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('teacher', 'style', 'teacher__category')

    def get_days(self, group):
        return group.get_days
    get_days.short_description = 'Дні'


class AbonementAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'duration']
    list_filter = ['category', 'number_of_lessons', 'duration']
    list_editable = ['price']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category')


class HallAdmin(admin.ModelAdmin):
    list_display = ['number', 'square', 'rent_price', 'rent_for_teachers']


class AbonementItemAdmin(admin.ModelAdmin):
    list_display = ['abonement_type', 'owner', 'is_active', 'activated_date', 'lessons_used']
    list_filter = ['is_active', 'abonement_type__number_of_lessons', 'abonement_type__category']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('owner', 'abonement_type', 'abonement_type__category')


class LessonAdmin(admin.ModelAdmin):
    list_display = ['group', 'num_of_students', 'date']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('group', 'group__teacher', 'group__style').prefetch_related('students').annotate(
            _num_of_students=Count('students'),
        )

    def num_of_students(self, lesson):
        return lesson._num_of_students
    num_of_students.short_description = 'Кількість'


admin.site.register(Style, StyleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Abonement, AbonementAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(AbonementItem, AbonementItemAdmin)
admin.site.register(Lesson, LessonAdmin)
