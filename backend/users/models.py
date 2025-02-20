from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.core.mail import send_mail

from users import constants as c


class User(AbstractUser):
    """Кастомная модель пользователя."""

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'Имя пользователя',
        max_length=c.LEN_USERNAME,
        unique=True,
        help_text=(
            'Обязательное поле. Не более 150 символов. '
            'Можно использовать буквы, цифры и спецсимволы: @/./+/-/_'
        ),
        validators=[username_validator],
        error_messages=dict(
            unique='Пользователь с таким именем пользователя уже существует.'
        ),
    )
    first_name = models.CharField('Имя', max_length=c.LEN_FIRSTNAME,)
    last_name = models.CharField('Фамилия', max_length=c.LEN_LASTNAME)
    email = models.EmailField('Email', max_length=c.LEN_EMAIL, unique=True)
    is_staff = models.BooleanField(
        'Сотрудник организации',
        default=False,
        help_text='Определяет, может ли пользоваться админкой.',
    )
    is_active = models.BooleanField(
        'Активен',
        default=True,
        help_text=(
            'Вместо удадения пользователя, можно его сделать неактивным.'
        ),
    )
    date_joined = models.DateTimeField('Дата посещения', default=timezone.now)
    avatar = models.ImageField(
        'Аватар',
        upload_to='users/avatars/',
        blank=True,
        null=True
    )
    subscriptions = models.ManyToManyField(
        'Подписки',
        symmetrical=False,
        related_name='subscribers',
        blank=True
    )
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='user_cart',
        verbose_name='Корзина'
    )
    favourites = models.ManyToManyField(
        'Recipe',
        blank=True,
        related_name='favorited_by',
        verbose_name='Избранное'
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Возвращает строку с именем и фамилией.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Возвращает только имя."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Отправка письма пользователю."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_subscribed(self):
        pass

    @property
    def is_favorite(self):
        pass

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
