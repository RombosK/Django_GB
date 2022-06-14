from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {"blank": True, "null": True}


class BaseModel(models.Model):  # base class should subclass 'django.db.models.Model'
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created_at"), editable=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="_(updated_at)", editable=False)
    deleted = models.BooleanField(default=False, verbose_name=_("deleted"))

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class NewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class News(BaseModel):
    objects = NewsManager()
    DoesNotExist = models.Manager

    title = models.CharField(max_length=256, verbose_name="title")
    preambule = models.CharField(max_length=1024, verbose_name=_("preambule"))
    body = models.TextField(blank=True, null=True, verbose_name=_("body"))
    body_as_markdown = models.BooleanField(default=False, verbose_name=_("as markdown"))

    def __str__(self) -> str:
        return f"{self.pk} {self.title}"

    class Meta:
        ordering = ("-created_at", "-updated_at")
        verbose_name = "новость"
        verbose_name_plural = "новости"


class Courses(BaseModel):
    name = models.CharField(max_length=256, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"), **NULLABLE)
    description_as_markdown = models.BooleanField(verbose_name=_("as markdown"), default=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("cost"), default=0)
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name=_("cover"))

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, **NULLABLE)
    num = models.PositiveIntegerField(verbose_name=_("lesson number"))
    title = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name=_("description"), **NULLABLE)
    description_as_markdown = models.BooleanField(verbose_name=_("as markdown"), default=False)

    def __str__(self) -> str:
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        ordering = ("course", "num")
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class CourseTeachers(BaseModel):
    course = models.ManyToManyField(Courses)
    name_first = models.CharField(max_length=128, verbose_name=_("name"))
    name_second = models.CharField(max_length=128, verbose_name=_("surname"))
    day_birth = models.DateField(verbose_name=_("day_birth"))

    def __str__(self) -> str:
        return f"{self.pk} {self.name_second} {self.name_first}"

    class Meta:
        verbose_name = "CourseTeacher"


class CourseFeedback(BaseModel):
    RAITING_FIVE = 5
    RAITING_FOUR = 4
    RAITING_THREE = 3
    RAITING_TWO = 2
    RAITING_ONE = 1

    RATINGS = (
        (RAITING_FIVE, '⭐⭐⭐⭐⭐'),
        (RAITING_FOUR, '⭐⭐⭐⭐'),
        (RAITING_THREE, '⭐⭐⭐'),
        (RAITING_TWO, '⭐⭐'),
        (RAITING_ONE, '⭐'),
    )

    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name=_('course'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    feedback = models.TextField(verbose_name='Отзыв', default=_('empty'))
    rating = models.PositiveSmallIntegerField(choices=RATINGS, default=RAITING_FIVE, verbose_name=_('rating'))

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f'Отзыв о курсе {self.course} от {self.user} '

