# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError('Users must have an email address')

        elif not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


@python_2_unicode_compatible
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name='username',
        max_length=30,
        unique=True,
    )
    name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'username': self.username})

    @property
    def is_staff(self):
        return self.is_admin

@python_2_unicode_compatible
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower')
    following = models.ForeignKey(User, related_name='following')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(
            self.follower.username,
            self.following.username
        )