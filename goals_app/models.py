from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.core import validators
from django.db import models
from django.utils.translation import ngettext_lazy
import jwt

from datetime import date, datetime, timedelta
from secrets import token_urlsafe


class CapitalizedCharField(models.CharField):
    def get_prep_value(self, value):
        print(value)
        return value.capitalize()


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Overrode to run password field validators on raw password.
        """
        self.model.validate_password(password)
        return super()._create_user(username, email, password, **extra_fields)


class User(AbstractUser):  # TODO: Check that username is required during the reg
    objects = CustomUserManager()

    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(
        max_length=128,
        validators=[
            validators.MinLengthValidator(
                settings.MIN_PASSWORD_LENGTH,
                ngettext_lazy(
                    'Ensure password has at least %(limit_value)d character '
                    '(it has %(show_value)d).',
                    'Ensure password has at least %(limit_value)d characters '
                    '(it has %(show_value)d).',
                    'limit_value'
                )
            )
        ]
    )

    USERNAME_FIELD = 'email'  # TODO: Inherit from AbstractBaseUser?
    REQUIRED_FIELDS = ['username']
    # TODO: Implement get_full_name and get_short_name.

    def __str__(self):
        return self.username

    @property
    def access_token(self):
        """
        Returns new access token on every invocation.
        """
        return self._generate_access_token()

    def _generate_access_token(self):
        dt = datetime.now() + timedelta(minutes=settings.JWT_LIFESPAN)
        token = jwt.encode({
            'id': self.pk,
            'exp': dt.timestamp()
        }, settings.SECRET_KEY, settings.JWT_SIGNING_ALGORITHM)
        return f'Bearer {token}'

    @property
    def refresh_token(self):
        return self._generate_refresh_token()

    def _generate_refresh_token(self):
        return RefreshToken.objects.create(user=self)

    def set_password(self, raw_password):
        """
        To force invocation of the field validators on raw password.
        As Django never saves raw password to DB, calling self.full_clean
        before super().set_password will result in validation of the hash of
        current password, calling it after will lead to validation of the hash
        of new password (not the password itself).
        """
        self.validate_password(raw_password)
        super().set_password(raw_password)

    @classmethod
    def validate_password(cls, value):
        """
        Runs password field validators on raw password.
        :param value: raw password
        """
        field_validators = cls._meta.get_field('password').validators
        for validator in field_validators:
            validator(value)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class TaskTemplate(models.Model):
    todo = CapitalizedCharField(max_length=100)  # TODO: Change to title
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField(default=date.today)
    finish_date = models.DateField()
    is_achieved = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.todo


class TaskManager(models.Manager):
    def create(self, *args, **kwargs):
        category = kwargs.get('category')
        if category:
            category = Category.objects.get_or_create(name=category)[0]
            kwargs['category'] = category
        return super().create(*args, **kwargs)

    def get_current_tasks(self, user_id):
        return self.filter(creator=user_id, is_achieved=False)


class Task(TaskTemplate):  # TODO: Add counter field.
    objects = TaskManager()

    reason = CapitalizedCharField(max_length=200)   # TODO: Make optional.
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, related_name='goals'
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='subtasks',
        null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if max_recursion_depth_exceeded(self, 'parent', 2):
            raise RecursionError('Maximum subtask nesting depth exceeded.')
        return super().save(*args, **kwargs)


class CategoryManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Category(models.Model):
    objects = CategoryManager()

    name = CapitalizedCharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Counter(models.Model):
    value = models.DecimalField(max_digits=12, decimal_places=2)
    target = models.DecimalField(max_digits=12, decimal_places=2)
    countable = models.CharField(max_length=30)

    @property
    def progress(self):
        return self.value / self.target

    @property
    def done(self):
        return self.value == self.target


class RefreshToken(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='refresh_tokens'
    )
    token = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.token

    def clean(self):
        super().clean()
        if not self.token:
            self.token = self._generate_token()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def _generate_token(self):
        return token_urlsafe(nbytes=48)

    def invalidate(self):
        self.delete()


def max_recursion_depth_exceeded(instance, parent_attr_name, max_depth):
    """
    Checks whether maximum recursion depth is exceeded.
    May fail if tree parent changes to one with depth < max_depth - 1.
    Temporary solution. Will move to django_mptt later.

    :param instance: Model instance.
    :param parent_attr_name: Attribute name to retrieve parent.
    :param max_depth: Max allowed tree level.
    :return: Bool
    """
    for step in range(max_depth + 1):
        instance = getattr(instance, parent_attr_name, None)
        if not instance:
            return False
    return True
