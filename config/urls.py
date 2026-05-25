from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),          # ← встроенная админка Django
    path('accounts/', include('accounts.urls')),
    path('', include('core.urls')),           # ← наши маршруты (должны быть после admin/)
]