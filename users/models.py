from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UnicodeUsernameValidator, UserManager
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import uuid

from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name=_('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(verbose_name=_('first name'), max_length=30)
    last_name = models.CharField(verbose_name=_('last name'), max_length=150)
    email = models.EmailField(verbose_name=_('email address'), blank=True)
    number = models.PositiveIntegerField(
        verbose_name=_('学籍番号'),
        unique=True,
        validators=[MinValueValidator(10000), MaxValueValidator(99999)]
    )
    wallet = models.PositiveIntegerField(verbose_name=_('所持金額'), default=0)

    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(verbose_name=_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'number']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class IDmField(models.CharField):
    description = _("FeliCa's IDm")
    default_validators = [
        RegexValidator(regex='^[0-9A-F]{16}$', message=_("IDm must be 16-digit hexadecimal number")),
        MinLengthValidator(16)
    ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', 'FeliCa ID')
        kwargs.setdefault('unique', True)
        kwargs['max_length'] = 16
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs


class Card(models.Model):
    is_guest = models.BooleanField(verbose_name='ゲスト', default=False)
    name = models.CharField(verbose_name='カード名', max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards', verbose_name='所持ユーザー')
    idm = IDmField()

    class Meta:
        verbose_name = _('ICカード')
        verbose_name_plural = _('ICカード')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Temporary(models.Model):
    idm = IDmField()
    uuid = models.UUIDField(verbose_name='UUID', default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = _('紐づけデータ')
        verbose_name_plural = _('紐づけデータ')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


def get_user_from_idm(idm):
    return User.objects.get(cards__idm=idm)
