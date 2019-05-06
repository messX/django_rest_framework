from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from pytz import unicode


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password):
        """
        Creates and saves a User with the given email and password
        """
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        if not password:
            raise ValueError('User must have a password')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    User profile which extends AbstractBaseUser class
    AbstractBaseUser contains basic fields like password and last_login
    """
    email = models.EmailField(
        verbose_name=_('Email'),
        max_length=getattr(settings, 'USER_EMAIL_MAX_LENGTH', 100),
        unique=True
    )
    username = models.CharField(
        verbose_name=_('Username'),
        max_length=getattr(settings, 'USER_USERNAME_MAX_LENGTH', 50),
        unique=True,
        null=False
    )
    is_active = models.BooleanField(
        verbose_name=_('Active'),
        default=True
    )
    is_admin = models.BooleanField(
        verbose_name=_('Admin'),
        default=False
    )
    date_joined = models.DateTimeField(
        verbose_name=_('Joined datetime'),
        auto_now_add=True,
        editable=False
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-id']

    def __unicode__(self):
        return unicode(self.email) or u''

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return not self.is_admin

    """
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
    """


class Article(models.Model):
    """
    Article information
    """
    author = models.ForeignKey(
        'User',
        related_name='articles',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=getattr(settings, 'ARTICLE_TITLE_MAX_LENGTH', 100)
    )
    context = models.TextField(
        verbose_name=_('Context'),
        max_length=getattr(settings, 'ARTICLE_CONTEXT_MAX_LENGTH', 100)
    )
    hits = models.PositiveIntegerField(
        verbose_name=_('Hits'),
        default=0
    )
    state_choices = (
        ('shown', 'Shown'),
        ('deleted', 'Deleted'),
    )
    state = models.CharField(
        verbose_name=_('State'),
        max_length=10,
        choices=state_choices,
        default='shown'
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created datetime'),
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated datetime'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ['-id']

    def __unicode__(self):
        return unicode(self.title) or u''


class Comment(models.Model):
    """
    Comment under specific article
    """
    article = models.ForeignKey(
        'Article',
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'User',
        related_name='comments',
        on_delete=models.CASCADE
    )
    context = models.TextField(
        verbose_name=_('Context'),
        max_length=getattr(settings, 'COMMENT_CONTEXT_MAX_LENGTH', 300)
    )
    state_choices = (
        ('shown', 'Shown'),
        ('deleted', 'Deleted'),
    )
    state = models.CharField(
        verbose_name=_('State'),
        max_length=10,
        choices=state_choices,
        default='shown'
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created datetime'),
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated datetime'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-id']

    def __unicode__(self):
        return unicode(self.id) or u''
