from importlib.resources import _

from django.contrib import admin
from django.utils.html import format_html

from mainapp.models import News, Courses, Lesson, CourseTeachers


# admin.site.register(News)
# admin.site.register(Courses)
# admin.site.register(Lesson)
# admin.site.register(CourseTeachers)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'preambule', 'created_at', 'slug', 'deleted')
    list_filter = ('created_at', 'updated_at', 'deleted')
    search_fields = ('title', 'body', 'preambule')
    list_per_page = 5
    actions = ['mark_deleted']

    def mark_deleted(self, request, queryset):
        queryset.update(deleted=True)

    mark_deleted.short_description = _('Пометить как удалённые')

    def slug(self, obj):
        return format_html(
            '<a href="http://127.0.0.1:8088/admin/mainapp/news/ {}/change/">{}</a>',
            obj.pk,
            obj.title
        )

    slug.short_description = 'Заголовок'


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at', 'updated_at', 'slug', 'deleted',)
    list_per_page = 5
    list_filter = ('created_at', 'updated_at', 'deleted')
    search_fields = ('name', 'description', 'cost')
    show_full_result_count = False

    def slug(self, obj):
        return format_html(
            '<a href="http://127.0.0.1:8088/admin/mainapp/courses/ {}/change/">{}</a>',
            obj.pk,
            obj.name
        )

    slug.short_description = 'Название курса'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'num', 'created_at', 'updated_at', 'deleted')
    list_per_page = 10
    list_filter = ('created_at', 'updated_at', 'deleted')
    search_fields = ('title', 'description')
    show_full_result_count = False


@admin.register(CourseTeachers)
class CourseTeachersAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'day_birth', 'deleted')
    list_per_page = 10
    list_filter = ('name_first', 'name_second')
    search_fields = ('name_first', 'name_second')
    show_full_result_count = False
