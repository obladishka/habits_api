from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Поле 'email' обязательно для заполнения.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    username = models.CharField(
        max_length=150, verbose_name="username", help_text="Enter your username", null=True, blank=True
    )
    email = models.EmailField(unique=True, verbose_name="email", help_text="Enter your email")
    tg_chat_id = models.CharField(
        max_length=50,
        verbose_name="telegram chat id",
        help_text="Enter your telegram chat id (NOT your username that starts with @)",
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username if self.username else self.email

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
