from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from users import constants as c
from users.managers import CustomManager
from users.validators import NotMeValidator


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        max_length=c.LEN_USERNAME,
        unique=True,
        null=False,
        blank=False,
        help_text=(
            'Обязательное поле. Не более 150 символов. '
            'Можно использовать буквы, цифры и спецсимволы: @/./+/-/_'
        ),
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Некорректный username',
                code='invalid_username',
            ),
            NotMeValidator
        ],
        error_messages=dict(
            unique='Пользователь с таким именем пользователя уже существует.'
        ),
        verbose_name='Имя пользователя'
    )
    first_name = models.CharField(
        max_length=c.LEN_FIRSTNAME,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=c.LEN_LASTNAME,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        max_length=c.LEN_EMAIL,
        null=False,
        blank=False,
        unique=True,
        verbose_name='E-mail')
    is_staff = models.BooleanField(
        default=False,
        help_text='Определяет, может ли пользоваться админкой.',
        verbose_name='Сотрудник организаци'
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            'Вместо удадения пользователя, можно его сделать неактивным.'
        ),
        verbose_name='Активен'
    )
    date_joined = models.DateTimeField('Дата посещения', default=timezone.now)
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар',
        help_text=f'Не более {c.MAX_FILE_SIZE / (1024 * 1024)} Мб'
    )
    subscriptions = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        symmetrical=False,
        related_name='subscribers',
        blank=True,
        verbose_name='Подписки'
    )
    favourites = models.ManyToManyField(
        'recipe.Recipe',
        blank=True,
        related_name='favorited_by',
        verbose_name='Избранное'
    )

    objects = CustomManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @classmethod
    def already_use(cls, kwargs):
        username = kwargs.get('username')
        email = kwargs.get('email')
        errors = dict()
        if cls.objects.filter(username=username).exclude(email=email).exists():
            errors['username'] = f'Username {username} уже используется.'
        if cls.objects.filter(email=email).exclude(username=username).exists():
            errors['email'] = f'Email {email} уже используется.'
        return errors
