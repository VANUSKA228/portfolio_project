from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # добавляем поле role в форму редактирования
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('role',)}),
    )
    # отображаем роль в списке пользователей
    list_display = ('username', 'email', 'role', 'is_staff')

admin.site.register(User, CustomUserAdmin)