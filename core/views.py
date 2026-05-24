from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User

def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    user = request.user
    if user.role == 'admin':
        # Администратор видит всех пользователей
        all_users = User.objects.all()
        return render(request, 'admin_profile.html', {'all_users': all_users})
    else:
        # Обычный пользователь видит свой профиль
        return render(request, 'user_profile.html', {'profile_user': user})