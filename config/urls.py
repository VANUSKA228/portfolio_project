from django.contrib import admin
from django.urls import path, include
from core.views import home   # импортируем главную страницу

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),   # регистрация, вход, выход
    path('', home, name='home'),                    # главная страница
    path('', include('core.urls')),                 # профили и всё остальное
]