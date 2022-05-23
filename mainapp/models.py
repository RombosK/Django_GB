from django.db import models, migrations


NULLABLE = {"blank": True, "null": True}


class BaseModel(models.Model):  # base class should subclass 'django.db.models.Model'
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан", editable=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлён", editable=False)
    deleted = models.BooleanField(default=False, verbose_name="Удалён")

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

    title = models.CharField(max_length=256, verbose_name="Title")
    preambule = models.CharField(max_length=1024, verbose_name="Вступление")
    body = models.TextField(blank=True, null=True, verbose_name="Наполнение")
    body_as_markdown = models.BooleanField(default=False, verbose_name="As markdown")

    def __str__(self) -> str:
        return f"{self.pk} {self.title}"

    class Meta:
        ordering = ("-created_at", "-updated_at")
        verbose_name = "новость"
        verbose_name_plural = "новости"


class Courses(BaseModel):
    name = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена", default=0)
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name="Обложка")

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"

    class Mena:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, **NULLABLE)
    num = models.PositiveIntegerField(verbose_name="Lesson number")
    title = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)

    def __str__(self) -> str:
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        ordering = ("course", "num")
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class CourseTeachers(BaseModel):
    course = models.ManyToManyField(Courses)
    name_first = models.CharField(max_length=128, verbose_name="Имя")
    name_second = models.CharField(max_length=128, verbose_name="Фамилия")
    day_birth = models.DateField(verbose_name="Дата рождения")

    def __str__(self) -> str:
        return f"{self.pk} {self.name_second} {self.name_first} {self.created_at}"




