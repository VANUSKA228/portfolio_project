from django.shortcuts import render, redirect
from django.contrib.auth import login, logout   # ← добавлен logout
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)          # сразу авторизуем после регистрации
            return redirect('profile')    # перенаправляем в профиль
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')