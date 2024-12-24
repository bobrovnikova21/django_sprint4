# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseBlog(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено"
    )

    class Meta:
        abstract = True


class Category(BaseBlog):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(unique=True,
                            verbose_name="Идентификатор",
                            help_text="Идентификатор страницы для URL; "
                                      "разрешены символы латиницы, "
                                      "цифры, дефис и подчёркивание."
                            )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(BaseBlog):
    name = models.CharField(max_length=256, verbose_name="Название места")

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Post(BaseBlog):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст", )
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text="Если установить дату "
                  "и время в будущем — "
                  "можно делать отложенные публикации."
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        related_name="posts"
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        verbose_name="Местоположение",
        null=True,
        blank=True,
        related_name="posts"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        null=True
    )
    image = models.ImageField(
        upload_to="media/",
        null=True,
        verbose_name="Картинка",
        blank=True,
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
        related_name="comment"
    )
    text = models.TextField(
        verbose_name="Текст комментария"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comment"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено"
    )
