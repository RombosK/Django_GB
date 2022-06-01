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
    list_per_page = 3

    def slug(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.title.lower().replace(' ', '-'),
            obj.title
        )
    slug.short_description = 'Заголовок'


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseTeachers)
class CourseTeachersAdmin(admin.ModelAdmin):
    pass
