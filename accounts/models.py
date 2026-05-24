from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # поле для выбора роли
    ROLE_CHOICES = (
        ('user', 'Обычный пользователь'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Роль'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"