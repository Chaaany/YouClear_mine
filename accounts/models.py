from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_no_special_characters

class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        validators=[validate_no_special_characters],
        error_messages={"unique": "이미 사용중인 닉네임입니다."},
    )

    address = models.CharField(
      max_length=50,
      null=True,
    )

    detail_address = models.CharField(
      max_length=50,
      blank=True,
      null=True,
    )


    def __str__(self):
        return self.email
