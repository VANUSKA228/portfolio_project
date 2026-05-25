from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from accounts.models import User
import logging

logger = logging.getLogger('admin_actions')

# ------------------------------------------------------------
# Главная страница
# ------------------------------------------------------------
def home(request):
    return render(request, 'home.html')


# ------------------------------------------------------------
# API для живого поиска пользователей (JSON)
# ------------------------------------------------------------
def search_users_api(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 1:
        return JsonResponse({'results': []})
    
    users = User.objects.filter(username__icontains=query)[:10]
    results = [
        {
            'id': user.id,
            'username': user.username,
            'role': user.get_role_display(),
        }
        for user in users
    ]
    return JsonResponse({'results': results})


# ------------------------------------------------------------
# Публичный профиль пользователя (доступен всем)
# ------------------------------------------------------------
def user_public_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    return render(request, 'public_profile.html', {'profile_user': profile_user})


# ------------------------------------------------------------
# Личный профиль (только для авторизованных, зависит от роли)
# ------------------------------------------------------------
@login_required
def profile(request):
    user = request.user
    if user.role == 'admin':
        all_users = User.objects.all().order_by('-date_joined')
        query = request.GET.get('q', '').strip()
        if query:
            all_users = all_users.filter(username__icontains=query)
        return render(request, 'admin_profile.html', {
            'all_users': all_users,
            'search_query': query,
        })
    else:
        return render(request, 'user_profile.html', {'profile_user': user})


# ------------------------------------------------------------
# Админ: удаление одного пользователя
# ------------------------------------------------------------
@login_required
def admin_delete_user(request, user_id):
    if request.user.role != 'admin':
        messages.error(request, 'Недостаточно прав.')
        return redirect('profile')

    target = get_object_or_404(User, id=user_id)

    if target == request.user:
        messages.error(request, 'Нельзя удалить самого себя.')
        return redirect('profile')

    username = target.username
    target.delete()

    logger.info(f'Админ {request.user.username} удалил пользователя {username}')
    messages.success(request, f'Пользователь {username} удалён.')
    return redirect('profile')


# ------------------------------------------------------------
# Админ: массовое удаление пользователей
# ------------------------------------------------------------
@login_required
def admin_bulk_delete(request):
    if request.user.role != 'admin':
        messages.error(request, 'Недостаточно прав.')
        return redirect('profile')

    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        if not user_ids:
            messages.warning(request, 'Не выбрано ни одного пользователя.')
            return redirect('profile')

        deleted_count = 0
        for user_id in user_ids:
            target = get_object_or_404(User, id=user_id)
            if target != request.user:
                target.delete()
                deleted_count += 1
                logger.info(f'Админ {request.user.username} удалил пользователя {target.username} (массово)')

        messages.success(request, f'Удалено пользователей: {deleted_count}.')
    return redirect('profile')


# ------------------------------------------------------------
# Админ: редактирование профиля пользователя
# ------------------------------------------------------------
@login_required
def admin_edit_user(request, user_id):
    if request.user.role != 'admin':
        messages.error(request, 'Недостаточно прав.')
        return redirect('profile')

    target = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        new_username = request.POST.get('username', '').strip()
        new_email = request.POST.get('email', '').strip()
        new_role = request.POST.get('role', '').strip()

        if new_username and new_username != target.username:
            if User.objects.filter(username=new_username).exclude(id=target.id).exists():
                messages.error(request, 'Пользователь с таким именем уже существует.')
                return redirect('profile')
            target.username = new_username

        if new_email:
            target.email = new_email

        if new_role in ['user', 'admin']:
            target.role = new_role

        target.save()
        logger.info(f'Админ {request.user.username} изменил профиль пользователя {target.username}')
        messages.success(request, f'Профиль {target.username} обновлён.')
        return redirect('profile')

    return render(request, 'admin_edit_user.html', {'target_user': target})


# ------------------------------------------------------------
# Админ: войти как пользователь (impersonation)
# ------------------------------------------------------------
@login_required
def admin_impersonate(request, user_id):
    if request.user.role != 'admin':
        messages.error(request, 'Недостаточно прав.')
        return redirect('profile')

    target = get_object_or_404(User, id=user_id)

    if target == request.user:
        messages.error(request, 'Вы уже в своём аккаунте.')
        return redirect('profile')

    # Сохраняем ID админа ДО логина под пользователем
    admin_id = request.user.id

    # Логинимся под целевым пользователем
    login(request, target)

    # ВАЖНО: записываем admin_id в сессию ПОСЛЕ логина
    request.session['original_admin_id'] = admin_id
    request.session.modified = True

    logger.info(f'Админ (id={admin_id}) вошёл как пользователь {target.username}')
    messages.info(request, f'Вы вошли как {target.username}. Для возврата нажмите "Выйти в админ-панель".')
    return redirect('profile')


# ------------------------------------------------------------
# Выход из режима impersonation (возврат в админку)
# ------------------------------------------------------------
@login_required
def admin_restore(request):
    admin_id = request.session.pop('original_admin_id', None)

    if admin_id:
        try:
            admin_user = User.objects.get(id=admin_id)
            login(request, admin_user)
            logger.info(f'Админ {admin_user.username} вернулся из режима impersonation')
            messages.success(request, 'Вы вернулись в режим администратора.')
        except User.DoesNotExist:
            logout(request)
            messages.error(request, 'Учётная запись администратора не найдена.')
            return redirect('home')
    else:
        logout(request)
        return redirect('home')

    return redirect('profile')